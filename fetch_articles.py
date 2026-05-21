"""
This document serves as a way to automize the download of articles from an online database, particularly
the PubMed (PMC) publicly available articles.

The code is separated into various functions with their own functionalities explained within their docstring.
However, the overall steps followed to obtain these articles is:

1. Search for articles in the specified date range (2000 - 2019), and obtain their IDs.
2. Using this ID, we obtain the article's full XML content via the API.
3. The content is "filtered" so that only the abstract and paragraphs remain.
4. From this text, the XML tags are removed to ensure that the output is clean text.
5. The content of each article is then saved into a .txt file which will be used as input in the notebook.

SOURCES
- https://docs.python.org/3/library/xml.etree.elementtree.html
- https://www.ncbi.nlm.nih.gov/books/NBK25499/
- https://lxml.de/tutorial.html
- https://www.ncbi.nlm.nih.gov/books/NBK25499/
- https://www.w3schools.com/python/python_file_write.asp
- https://claude.ai/share/e7277672-2d81-46ac-965d-b01704ce3a05
"""
import os
import time
import requests
from lxml import etree

# How many articles we want and the dates we want them within
article_number = 200
date_range = "2000:2019"

# Making a new directory to store the output
# Folder containing .txt files with articles
output_directory = "all_articles"
os.makedirs(output_directory, exist_ok=True)

# Get the ids and get the content associated to the id
esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
efetch  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# ------------------------------------------------
def search_pmc(max_results, retstart=0):
    """
    Search PMC and return a list of ids matching the date range.
    retstart lets us page through results when filtering rejects some.
    """
    params = {
        "db": "pmc",
        "term": f"open access[filter] AND {date_range}[pdat]",
        "retmax": max_results,
        "retstart": retstart,
        "retmode": "xml",
    }

    # Get the HTTP response and parse XML to form tree
    r = requests.get(esearch, params=params, timeout=30)
    root = etree.fromstring(r.content)

    # Extract ids from anywhere in the tree
    ids = []
    for id_i in root.findall(".//Id"):
        ids.append(id_i.text)
    return ids

# ------------------------------------------------
def fetch_article_xml(pmcid):
    """
    Fetch XML for a single article.
    """
    params = {
        "db": "pmc",
        "id": pmcid,
        "retmode": "xml"
    }
    r = requests.get(efetch, params=params, timeout=30)
    return r.content

# ------------------------------------------------
def clean_text(element):
    """
    Remove the XML tags and collapse whitespace, so inline elements like
    <xref> citations don't end up on their own line.
    """
    return " ".join("".join(element.itertext()).split())

# ------------------------------------------------
def parse_abstract(xml_tree):
    """
    Extract abstract text from the XML tree.
    """
    abstract = xml_tree.find(".//abstract")

    # Had to add this check it was returning an error
    if abstract is None:
        return ""
    
    return clean_text(abstract)

# ------------------------------------------------
def parse_body(xml_tree):
    """
    Return body paragraphs <p> inside each section.
    """
    parts = []
    body = xml_tree.find(".//body")

    if body is None:
        return ""

    # Loop over the sections that are part of the body
    for section in body.iter():

        # Extract paragraph tags for each section
        if section.tag == "p" and section.getparent().tag in ("sec", "body"):
            parts.append(clean_text(section))

    # Newline to separate paragraphs
    return "\n".join(parts)

# ------------------------------------------------
def format_article(abstract, body):
    """
    Combine all extracted parts.
    """
    return "\n\n".join([abstract, body])

# ------------------------------------------------
def write_to_file(text, output_path):
    """
    Write text into a .txt file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

# ------------------------------------------------
def main():
    saved = 0
    seen = set()
    retstart = 0

    # Keep fetching more pages until we have the target number of valid papers
    while saved < article_number:
        pmcids = search_pmc(article_number, retstart=retstart)
        if not pmcids:
            print("no more results from pubmed")
            break
        retstart += len(pmcids)

        for pmcid in pmcids:
            if saved >= article_number:
                break
            if pmcid in seen:
                continue
            seen.add(pmcid)

            # Skip if already saved locally so re-runs don't redownload existing papers
            output_path = os.path.join(output_directory, f"PMC{pmcid}.txt")
            if os.path.exists(output_path):
                saved += 1
                print(f"[{saved}/{article_number}] PMC{pmcid} (kept)")
                continue

            xml = fetch_article_xml(pmcid)
            try:
                root = etree.fromstring(xml)
            except etree.XMLSyntaxError:
                print(f"PMC{pmcid} skipped: malformed XML response")
                continue

            # Skip corrections, reviews, editorials etc, we only want research articles
            article = root.find(".//article")
            if article is None or article.get("article-type") != "research-article":
                print(f"PMC{pmcid} skipped: not a research article")
                continue

            abstract = parse_abstract(root)
            body = parse_body(root)

            # Skip papers where body parsing returned nothing
            if not body.strip():
                print(f"PMC{pmcid} skipped: no body content")
                continue

            # Skip papers without an abstract
            if not abstract.strip():
                print(f"PMC{pmcid} skipped: no abstract")
                continue

            text = format_article(abstract, body)

            # Skip papers too long for the rewrite stage (Vertex TPM caps choke on huge papers)
            if len(text) > 60_000:
                print(f"PMC{pmcid} skipped: too long ({len(text)} chars)")
                continue

            write_to_file(text, os.path.join(output_directory, f"PMC{pmcid}.txt"))
            saved += 1

            print(f"[{saved}/{article_number}] PMC{pmcid}")

            # Limit of requests so we need to pause
            time.sleep(0.4)

    print(f"\ndone: saved {saved}/{article_number} papers")

if __name__ == "__main__":
    main()

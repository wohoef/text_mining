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
article_number = 50
date_range = "2000:2019"

# Making a new directory to store the output
# Folder containing .txt files with articles
output_directory = "pmc_articles"
os.makedirs(output_directory, exist_ok=True)

# Get the ids and get the content associated to the id
esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
efetch  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# ------------------------------------------------
def search_pmc(max_results):
    """
    Search PMC and return a list of ids matching the date range.
    """
    params = {
        "db": "pmc",
        "term": f"open access[filter] AND {date_range}[pdat]",
        "retmax": max_results,
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
    Remove the XML tags.
    """
    return "".join(element.itertext())

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
        if section.tag == "p" and section.getparent().tag == "sec":
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
    pmcids = search_pmc(article_number)

    for i, pmcid in enumerate(pmcids, 1):
        xml = fetch_article_xml(pmcid)
        root = etree.fromstring(xml)
        abstract = parse_abstract(root)
        body = parse_body(root)
        text = format_article(abstract, body)
        write_to_file(text, os.path.join(output_directory, f"PMC{pmcid}.txt"))

        print(f"[{i}/{len(pmcids)}] PMC{pmcid}")

        # Limit of requests so we need to pause
        time.sleep(0.4)

if __name__ == "__main__":
    main()

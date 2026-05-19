from collections import Counter
import statistics
import spacy

_nlp = spacy.load("en_core_web_sm")


# AI-marker words based on literature
AI_MARKER_WORDS = {
    "align",
    "aligned",
    "aligning",
    "aligns",
    "crucial",
    "crucially",
    "delve",
    "delved",
    "delves",
    "delving",
    "excel",
    "excelled",
    "excelling",
    "excels",
    "finding",
    "findings",
    "garner",
    "garnered",
    "garnering",
    "garners",
    "grapple",
    "grappled",
    "grapples",
    "grappling",
    "intricate",
    "intricately",
    "meticulous",
    "meticulously",
    "notable",
    "notably",
    "offer",
    "offered",
    "offering",
    "offers",
    "pivotal",
    "potential",
    "potentials",
    "realm",
    "realms",
    "showcase",
    "showcased",
    "showcases",
    "showcasing",
    "underscore",
    "underscored",
    "underscores",
    "underscoring",
}

# ------------------------------------------------
# Aux 1
def get_words(x):
    """
    Returns a list of words from the list of sentences x.
    """
    words = []
    for sentence in x:
        for word in sentence:
            if word.isalpha():
                words.append(word.lower())
    return words

# ------------------------------------------------
# Aux 2
def sliding_window(l, n):
    """
    Slides a window of size n across list l, where each window is a list.
    This allows us to have more training samples.

    Example for n=2:
    ABCDE -> AB, BC, CD, DE
    """
    window = l[:n-1]
    for e in l[n-1:]:
        window.append(e)
        yield window[::]
        window.pop(0)

# ------------------------------------------------
# Aux 3
_doc_cache = {}

def _get_doc(sentence):
    key = tuple(sentence)
    if key not in _doc_cache:
        _doc_cache[key] = _nlp(" ".join(sentence))
    return _doc_cache[key]

# ------------------------------------------------
# Feature 1
def av_element_length(x):
    """
    Returns the average length of the elements in the list x. Used for our list
    of sentences or list of words.
    """
    lengths = [len(element) for element in x]

    return sum(lengths)/len(lengths)

# ------------------------------------------------
# Feature 2
def av_word_length(x):
    """
    Returns the average word length (in characters) across all sentences in x,
    where x is a list of sentences and each sentence is a list of words.
    """
    words = get_words(x)

    return av_element_length(words)

# ------------------------------------------------
# Feature 3
def type_token_ratio(x):
    """
    Returns the type-token ratio of the list x. This means the ratio of unique words to total words.
    """
    words = get_words(x)

    return len(set(words)) / len(words)

# ------------------------------------------------
# Feature 4
def burstiness(x):
    """
    Returns the burstiness of the list x. We measure this as the coefficient
    of the standard deviation of sentence lengths.
    """
    lengths = [len(element) for element in x]
    mean = statistics.mean(lengths)
    stdev = statistics.stdev(lengths)

    return stdev / mean


# ------------------------------------------------
# Feature 5
def _token_depth(token):
    """
    Returns the depth of the subtree
    """
    children = list(token.children)
    if len(children) == 0:
        return 1
    return 1 + max(_token_depth(child) for child in children)

_depth_cache = {}

def _sentence_depth(sentence):
    """
    Returns the parse tree depth of a sentence.
    """
    key = tuple(sentence)
    if key in _depth_cache:
        return _depth_cache[key]

    doc = _get_doc(sentence)
    sent = next(doc.sents)
    depth = _token_depth(sent.root)
    _depth_cache[key] = depth
    return depth

def av_parse_tree_depth(x):
    """
    Returns the average dependency parse tree depth.
    """
    return sum(_sentence_depth(sentence) for sentence in x) / len(x)

# Feature 6 (multiple similar ones)
_function_word_groups = {
    "pron": ["PRON"],
    "adp":  ["ADP"],
    "det":  ["DET"],
    "conj": ["CCONJ", "SCONJ"],
    "aux":  ["AUX"],
}

def function_word_rates(x):
    """
    Returns a dict mapping each function word group to its rate
    (function word count / number of tokens).
    """
    counts = {group: 0 for group in _function_word_groups}
    total = 0
    for sentence in x:
        doc = _get_doc(sentence)
        for token in doc:
            if not token.is_alpha:
                continue
            total += 1
            for group, tags in _function_word_groups.items():
                if token.pos_ in tags:
                    counts[group] += 1
                    break
    if total == 0:
        return {group: 0.0 for group in _function_word_groups}
    return {group: counts[group] / total for group in _function_word_groups}

# ------------------------------------------------
# Feature 7
def ai_marker_word_rate(x):
    """
    Returns the proportion of words that belong to a fixed list of
    AI-associated vocabulary.
    """
    words = get_words(x)
    if len(words) == 0:
        return 0.0

    marker_count = sum(word in AI_MARKER_WORDS for word in words)
    return marker_count / len(words)

# ------------------------------------------------
# Feature 8
def learn_ai_excess_words(ai_corpus, human_corpus, top_n=50, min_count=3):
    """
    Learns words that are disproportionately common in AI text compared to
    human text. This should be called only on the training corpus to avoid
    leaking test-set information into the feature extraction step.
    """
    ai_counts = Counter()
    human_counts = Counter()

    for article in ai_corpus:
        ai_counts.update(get_words(article))

    for article in human_corpus:
        human_counts.update(get_words(article))

    ai_total = sum(ai_counts.values())
    human_total = sum(human_counts.values())
    vocabulary = set(ai_counts) | set(human_counts)
    vocab_size = len(vocabulary)
    scores = {}

    for word in vocabulary:
        total_count = ai_counts[word] + human_counts[word]
        if total_count < min_count:
            continue

        ai_rate = (ai_counts[word] + 1) / (ai_total + vocab_size)
        human_rate = (human_counts[word] + 1) / (human_total + vocab_size)
        scores[word] = ai_rate / human_rate

    top_words = sorted(scores, key=scores.get, reverse=True)[:top_n]
    return set(top_words), scores

def learned_ai_vocab_rate(x, ai_excess_words):
    """
    Returns the proportion of words that belong to a learned list of words
    with excess usage in AI text.
    """
    words = get_words(x)
    if len(words) == 0:
        return 0.0

    marker_count = sum(word in ai_excess_words for word in words)
    return marker_count / len(words)

# ------------------------------------------------
def extract_features(corpus, human, ai_excess_words=None):
    """
    Extracts features from the corpus using a sliding window of 5 sentences and returns
    the features and the labels. Returns two lists: X and Y where X contains the features and
    Y contains the labels for each 5-sentence list.
    """
    # raw_X will contain all the 5-sentence lists
    raw_X, X, Y = [], [], []

    # Slide window across corpus to make training samples of 5 sentences and store them in raw_X.
    # Each sample is labeled as human (1) or AI (0) and stored in Y.
    for passage  in sliding_window(corpus, 5):
        raw_X.append(passage)
        Y.append(int(human))

    # For each sample compute the features (as vectors) and store them in X.
    for x in raw_X:
        sample = []
        sample.append(av_element_length(x)) # Average number of words per sentence
        sample.append(av_word_length(x)) # Average number of characters per word
        sample.append(type_token_ratio(x)) # Vocabulary uniqueness
        sample.append(burstiness(x)) # Variation in sentence lengths
        sample.append(av_parse_tree_depth(x))
        sample.append(ai_marker_word_rate(x))
        if ai_excess_words is not None:
            sample.append(learned_ai_vocab_rate(x, ai_excess_words))
        rates = function_word_rates(x)
        sample += [rates[key] for key in rates]
        X.append(sample)

    return X, Y

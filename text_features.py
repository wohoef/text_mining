import statistics

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
def extract_features(corpus, human):
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
        X.append(sample)
    
    return X, Y
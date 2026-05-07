def sliding_window(l, n):
        """
        Example for n=2
        ABCDE -> AB, BC, CD, DE
        """
        window = l[:n-1]
        for e in l[n-1:]:
            window.append(e)
            yield window[::]
            window.pop(0)

def av_element_length(x):
        lengths = [len(y) for y in x]
        return sum(lengths)/len(lengths)

def av_word_length(x):
    words = [word for sentence in x for word in sentence]
    return av_element_length(words)

def extract_features(corpus, human):
    # raw_X will contain all the 5-sentence lists
    raw_X, X, Y = [], [], []

    # Populate raw_X and Y
    for passage  in sliding_window(corpus, 5):
        raw_X.append(passage)
        Y.append(int(human))

    # Populate X
    for x in raw_X:
        sample = []
        sample.append(av_element_length(x)) # Av sentence length
        sample.append(av_word_length(x))
        X.append(sample)
    
    return X, Y
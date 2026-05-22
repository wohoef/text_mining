# Model functions
"""
Shared helpers for loading corpora and building model datasets.

The important rule for paired human/AI data is that both versions of an article
use the same train/test split. The load_corpus function can create a shuffled
split once, then reuse the same filenames for the matching AI folder.
"""

from pathlib import Path
import random

import nltk

from scripts.text_features import extract_features, learn_ai_excess_words

def load_corpus(folder):
    """
    Loads a corpus from a folder of .text files, and returns a train and test set. Each set 
    contains a list of articles where each article is a list of sentences and each sentence is
    a list of words.
    """
    corpus = []
    
    for path in sorted(Path(folder).iterdir()):
        
        # Load the raw text
        raw_text = open(path, 'r', encoding='utf-8', errors='ignore').read()
        
        # Split the text into sentences
        sentences = nltk.sent_tokenize(raw_text)
        
        # Split each sentence into words
        article = [nltk.word_tokenize(sentence) for sentence in sentences] 
        corpus.append(article)   

    random.seed(26)
    random.shuffle(corpus)
    
    # 70/30 train/test split
    split = int(len(corpus)*0.7)
    train = corpus[:split]
    test = corpus[split:]
    
    return train, test


def learn_training_ai_excess_words(ai_corpus_train, human_corpus_train, top_n=50, min_count=3):
    """
    Learns AI-excess words from training articles only.
    """
    return learn_ai_excess_words(
        ai_corpus_train,
        human_corpus_train,
        top_n=top_n,
        min_count=min_count,
    )


def build_dataset_with_groups(human_corpus, ai_corpus, ai_excess_words=None):
    """
    Builds X, Y, and article-pair group IDs for grouped cross-validation.
    """
    if len(human_corpus) != len(ai_corpus):
        raise ValueError("Human and AI corpora must have the same number of aligned articles.")

    X, Y, groups = [], [], []

    for group_id, (human_article, ai_article) in enumerate(zip(human_corpus, ai_corpus)):
        human_X, human_Y = extract_features(
            human_article,
            True,
            ai_excess_words=ai_excess_words,
        )
        X.extend(human_X)
        Y.extend(human_Y)
        groups.extend([group_id] * len(human_Y))

        ai_X, ai_Y = extract_features(
            ai_article,
            False,
            ai_excess_words=ai_excess_words,
        )
        X.extend(ai_X)
        Y.extend(ai_Y)
        groups.extend([group_id] * len(ai_Y))

    return X, Y, groups

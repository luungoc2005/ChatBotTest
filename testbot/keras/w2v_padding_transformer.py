import numpy as np
import string
import pickle
import os
from collections import defaultdict
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.spatial import distance
from nltk import wordpunct_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
# from sklearn.feature_extraction.text import TfidfVectorizer

WORD2VEC = None
WORD2VEC_FILE = 'glove/glove.6B.50d'

def init_w2v():
    global WORD2VEC
    if not WORD2VEC:
        if os.path.isfile(WORD2VEC_FILE + '.pickle'):
            print('Importing %s...' % (WORD2VEC_FILE + '.pickle'))
            with open(WORD2VEC_FILE + '.pickle', 'rb') as pickle_file:
                WORD2VEC = pickle.load(pickle_file)
        else:
            print('Importing %s...' % (WORD2VEC_FILE + '.txt'))
            with open(WORD2VEC_FILE + '.txt', 'r') as lines:
                WORD2VEC = {
                    line.split()[0]: np.array(list(map(float, line.split()[1:])), dtype='float16')
                    for line in lines
                }
            with open(WORD2VEC_FILE + '.pickle', 'wb') as pickle_file:
                pickle.dump(WORD2VEC, pickle_file)
    return WORD2VEC

def measure_dist(word1, word2):
    global WORD2VEC
    if not WORD2VEC:
        init_w2v()
    return np.linalg.norm(WORD2VEC[word1] - WORD2VEC[word2])

def print_top_similar(word):
    global WORD2VEC
    if not WORD2VEC:
        init_w2v()
    all_words = list([
        [test_word, np.linalg.norm(WORD2VEC[test_word] - WORD2VEC[word])]
        for test_word in WORD2VEC.keys()
    ])
    all_words = sorted(all_words, key=lambda item: item[1])
    return all_words[0:15]

class Word2VecVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self, word2vec=None, sent_size=50):
        self.word2vec = word2vec or init_w2v()
        # self.punct = list(set(string.punctuation))
        self.sent_size = sent_size
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.w2v_dim = len(iter(self.word2vec.values()).__next__())
        # self.punct_length = len(self.punct)
        self.dim =  self.w2v_dim # + self.punct_length

    # def get_weight(self, punct):
    #     return np.append(np.zeros(self.w2v_dim, dtype='float16'),
    #         np.array([1.0 if punct == X else 0.0 for X in self.punct], dtype='float16'))

    def transform_single(self, w):
        # return np.pad(self.word2vec[w], (0, self.punct_length), 'constant') \
        #     if w in self.word2vec.keys() \
        #     else self.get_weight(w)
        return self.word2vec[w] \
            if w in self.word2vec.keys() \
            else np.zeros(self.dim, dtype='float16')

    def inverse_transform_single(self, X):
        # X_vec = X[:self.w2v_dim]
        if np.any(X):
            min_dist = None
            min_word = ''
            for word in self.word2vec.keys():
                dist = np.linalg.norm(self.word2vec[word] - X)
                # dist = distance.euclidean(self.word2vec[word], X_vec)
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    min_word = word
            return min_word
        else:
            return ''
            # indice = np.nonzero(X[self.w2v_dim:])
            # if not indice:
            #     return ''
            # else:
            #     return self.punct[indice[0]]

    def fit(self, X, y):
        return self

    def transform(self, X):
        if not X:
            return np.zeros((self.sent_size, self.dim), dtype='float16')
        return [
            list(self.transform_sent(doc)) for doc in X
        ]
    
    def transform_sent(self, X):
        for sent in sent_tokenize(X):
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                yield self.transform_single(token.lower())
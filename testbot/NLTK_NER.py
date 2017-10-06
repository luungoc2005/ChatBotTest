import string
import nltk
import os

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.chunk import ne_chunk, conlltags2tree
from nltk.tree import Tree

from sklearn.base import BaseEstimator, TransformerMixin

class NLTK_NER_Chunker(BaseEstimator, TransformerMixin):

  def __init__(self, punct=None):
    self.punct = punct or set(string.punctuation)

  def fit(self, X, y=None):
    return self

  def inverse_transform(self, X):
    return [" ".join(doc) for doc in X]

  def transform(self, X):
    return [
      list(self.chunk(doc)) for doc in X
    ]

  def chunk(self, document):
    for sent in sent_tokenize(document):
      tokenized_text = wordpunct_tokenize(sent)
      tagged_words = pos_tag(tokenized_text)
      sent_tree = ne_chunk(tagged_words)

      for subtree in sent_tree:
        if type(subtree) == Tree:
          ne_label = subtree.label()
          ne_string = " ".join([token for token, pos in subtree.leaves()])
          yield (ne_string, ne_label)
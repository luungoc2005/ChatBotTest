import string
import nltk
import os

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.chunk import ne_chunk, conlltags2tree
from nltk.tree import Tree

from sklearn.base import BaseEstimator, TransformerMixin

def load_stanford_tagger():
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  STANDFORD_NER = os.path.join(BASE_DIR, 'stanford-ner-2017-06-09/')
  return StanfordNERTagger(
          os.path.join(STANDFORD_NER, 'classifiers/english.muc.7class.distsim.crf.ser.gz'),
          os.path.join(STANDFORD_NER, 'stanford-ner.jar'),
          encoding='utf-8')

class Stanford_NER_Chunker(BaseEstimator, TransformerMixin):

  def __init__(self, punct=None, tagger=None):
    self.punct = punct or set(string.punctuation)
    
    if (tagger == None):
      self.st_tagger = load_stanford_tagger()
    else:
      self.st_tagger = tagger

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
      tagged_words = self.stanford_tagger(tokenized_text)
      bio_tagged = self.bio_tagger(tagged_words)
      sent_tree = self.stanford_tree(bio_tagged)

      for subtree in sent_tree:
        if type(subtree) == Tree:
          ne_label = subtree.label()
          ne_string = " ".join([token for token, pos in subtree.leaves()])
          yield (ne_string, ne_label)
  
  def bio_tagger(self, ne_tagged):
    bio_tagged = []
    prev_tag = "O"
    for token, tag in ne_tagged:
      if tag == "O": #O
        bio_tagged.append((token, tag))
        prev_tag = tag
        continue
      if tag != "O" and prev_tag == "O": # Begin NE
        bio_tagged.append((token, "B-"+tag))
        prev_tag = tag
      elif prev_tag != "O" and prev_tag == tag: # Inside NE
        bio_tagged.append((token, "I-"+tag))
        prev_tag = tag
      elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
        bio_tagged.append((token, "B-"+tag))
        prev_tag = tag
    return bio_tagged

  def stanford_tree(self, bio_tagged):
    tokens, ne_tags = zip(*bio_tagged)
    pos_tags = [pos for token, pos in pos_tag(tokens)]

    conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
    ne_tree = conlltags2tree(conlltags)
    return ne_tree

  # Stanford NER tagger    
  def stanford_tagger(self, token_text):
    ne_tagged = self.st_tagger.tag(token_text)
    return(ne_tagged)
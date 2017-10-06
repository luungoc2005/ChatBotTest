from .NLTKPreprocessor import NLTKPreprocessor
from .Stanford_NER import Stanford_NER_Chunker
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
stopwords = []

def load_stopwords():
  fileinfo = open(os.path.join(BASE_DIR, 'stopwords.txt'), 'r')
  content = fileinfo.readlines()
  fileinfo.close()
  return [line.strip() for line in content if line.strip() != '']

def identity(arg):
    return arg

def tokenize_text(text):
  global stopwords
  preprocessor = NLTKPreprocessor(stopwords=stopwords)
  chunker = Stanford_NER_Chunker()
  # preprocessor = NLTKPreprocessor() # default stopwords
  if len(stopwords) == 0:
    stopwords = load_stopwords()
  # vectorizer = TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)
  
  preprocessed = preprocessor.transform([text])
  chunked = chunker.transform([text])
  data = {
    'preprocessed': preprocessed,
    'chunked': chunked
  }
  return json.dumps(data, sort_keys=True, indent=4)
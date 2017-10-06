from .NLTKPreprocessor import NLTKPreprocessor
from .Stanford_NER import Stanford_NER_Chunker, load_stanford_tagger
from .NLTK_NER import NLTK_NER_Chunker
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STANFORD_TAGGER = load_stanford_tagger()
STOPWORDS = []

def load_stopwords():
  fileinfo = open(os.path.join(BASE_DIR, 'stopwords.txt'), 'r')
  content = fileinfo.readlines()
  fileinfo.close()
  return [line.strip() for line in content if line.strip() != '']

def identity(arg):
    return arg

def tokenize_text(text):
  global STOPWORDS, STANFORD_TAGGER
  preprocessor = NLTKPreprocessor(stopwords=STOPWORDS)
  chunker = Stanford_NER_Chunker()
  # chunker = NLTK_NER_Chunker()
  # preprocessor = NLTKPreprocessor() # default stopwords
  if len(STOPWORDS) == 0:
    STOPWORDS = load_stopwords()
  # vectorizer = TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)
  
  preprocessed = preprocessor.transform([text])
  chunked = chunker.transform([text])
  data = {
    'preprocessed': preprocessed,
    'entities': chunked
  }
  return json.dumps(data, sort_keys=True, indent=4)
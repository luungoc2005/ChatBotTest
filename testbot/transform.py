from .NLTKPreprocessor import NLTKPreprocessor
from .entities.Stanford_NER import Stanford_NER_Chunker, load_stanford_tagger
from .entities.NLTK_NER import NLTK_NER_Chunker
from sklearn.feature_extraction.text import TfidfVectorizer
from recurrent import RecurringEvent
from datetime import datetime
from .train import test_model
import pytz
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOPWORDS = []


def load_stopwords():
    fileinfo = open(os.path.join(BASE_DIR, 'stopwords.txt'), 'r')
    content = fileinfo.readlines()
    fileinfo.close()
    return [line.strip() for line in content if line.strip() != '']


def identity(arg):
    return arg


def tokenize_text(text):
    global STOPWORDS
    r = RecurringEvent(now_date=datetime.now(pytz.utc))
    load_stanford_tagger()
    chunker = Stanford_NER_Chunker()
    # chunker = NLTK_NER_Chunker()
    # preprocessor = NLTKPreprocessor() # default stopwords
    if len(STOPWORDS) == 0:
        STOPWORDS = load_stopwords()
    # preprocessor = NLTKPreprocessor(stopwords=STOPWORDS)
    # vectorizer = TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)

    # preprocessed = preprocessor.transform([text])
    chunked = chunker.transform([text])
    named_entities = []
    
    for sentence in chunked:
        for (text, tag) in sentence:
            item = {
                'text': text,
                'entity': tag,
            }
            if tag in ['sys.date', 'sys.time']:
                date_result = r.parse(text)
                if date_result:
                    item['resolution'] = date_result.isoformat()
            named_entities.append(item)

    data = {
        # 'preprocessed': preprocessed,
        'classification': test_model(text),
        'entities': named_entities
    }
    return data


def test_transform(data):
    global STOPWORDS
    if len(STOPWORDS) == 0:
        STOPWORDS = load_stopwords()
    preprocessor = NLTKPreprocessor(stopwords=STOPWORDS)
    vectorizer = TfidfVectorizer(
        tokenizer=identity, preprocessor=None, lowercase=False)

    preprocessed = preprocessor.fit_transform(data)

    return vectorizer.fit_transform(preprocessed)

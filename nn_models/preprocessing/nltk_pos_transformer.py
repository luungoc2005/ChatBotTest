import string

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag

from sklearn.base import BaseEstimator, TransformerMixin


class NLTKPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, strip=True):
        self.strip = strip
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(sw.words('english'))

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [' '.join(doc[0]) for doc in X]

    def transform(self, X):
        return [
            list(self.tokenize(doc)) for doc in X
        ]

    def tokenize(self, document):
        for sent in sent_tokenize(document):
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                token = token.strip() if self.strip else token
                # token = token.strip('_') if self.strip else token
                # token = token.strip('*') if self.strip else token

                if token.lower() in self.stopwords:
                    yield ('', tag)
                else:
                    yield (self.lemmatize(token, tag), tag)
                # lemma = self.lemmatize(token, tag)
                # yield lemma

    def lemmatize(self, token, tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

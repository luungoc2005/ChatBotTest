from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from .NLTKPreprocessor import NLTKPreprocessor
from .models import Topic, Intent, Example
import os
import pickle
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINED_MODEL = None
STOPWORDS = []


def timeit(func):
    """
    Simple timing decorator
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        delta = time.time() - start
        return result, delta
    return wrapper


def load_stopwords():
    fileinfo = open(os.path.join(BASE_DIR, 'stopwords.txt'), 'r')
    content = fileinfo.readlines()
    fileinfo.close()
    return [line.strip() for line in content if line.strip() != '']


def identity(arg):
    return arg


def build_and_evaluate(x, y,
                       classifier=None, evaluate=True, outpath=None,
                       ignore_type=['N']):
    @timeit
    def build(classifier, X, y=None):
        global STOPWORDS

        if classifier == None:
            classifier = SGDClassifier(loss='log', max_iter=1000)

        if isinstance(classifier, type):
            classifier = classifier()

        if len(STOPWORDS) == 0:
            STOPWORDS = load_stopwords()

        model = Pipeline([
            ('preprocessor', NLTKPreprocessor(
                stopwords=STOPWORDS, ignore_type=ignore_type)),
            ('vectorizer', TfidfVectorizer(
                tokenizer=identity, preprocessor=None, lowercase=False
            )),
            ('classifier', classifier),
        ])

        model.fit(X, y)
        return model

    # Label encode the targets
    labels = LabelEncoder()
    y = labels.fit_transform(y)

    if evaluate == True:
        X_train, X_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2)
        (model, secs) = build(classifier, X_train, y_train)

        print("Evaluation model fit in {:0.3f} seconds".format(secs))
        print("Classification Report:\n")

        y_pred = model.predict(X_test)
        print(classification_report(y_test, y_pred, target_names=labels.classes_))

    model, secs = build(classifier, x, y)
    model.labels_ = labels

    print("Complete model fit in {:0.3f} seconds".format(secs))

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

        print("Model written out to {}".format(outpath))

    return model


def build_all(outpath=None):
    print("Fetching all data")
    data = \
        [{
            'text': item.text,
            'topic': item.intent.topic.name,
        } for item in list(Example.objects.all())]

    print("Training the topic classifier")
    model = {}
    model['topic_clf'] = build_and_evaluate([
        item['text'] for item in data
    ],
        [
            item['topic'] for item in data
    ], evaluate=False, ignore_type=[])

    model['topics'] = {}
    for topic in list(Topic.objects.all()):
        print("Training for topic %s:" % topic.name)
        data = []

        for intent in list(topic.intent_set.all()):
            data.extend([{
                'text': item.text,
                'intent': intent.name
            } for item in intent.example_set.all()])

        # print(data)
        model['topics'][topic.name] = build_and_evaluate([
            item['text'] for item in data
        ],
            [
                item['intent'] for item in data
        ], evaluate=False)

    if outpath == None:
        outpath = os.path.join(BASE_DIR, 'model.clf')

    print("Dumping model to %s" % outpath)
    with open(outpath, 'wb') as f:
        pickle.dump(model, f)

    print("Model written out to {}".format(outpath))

    return model


def test_model(text=''):
    def result_from_model(model, user_msg, model_name='Model'):
        yhat_proba = model.predict_proba([user_msg])
        labels_data = []

        for (idx, intent_proba) in enumerate(yhat_proba[0]):
            labels_data.append(
                [model.labels_.inverse_transform([idx])[0], intent_proba])

        labels_data = sorted(
            labels_data, key=lambda item: item[1], reverse=True)

        # for line in labels_data:
        #     print("%s %s - Confidence: %s" % (model_name, line[0], line[1]))

        return labels_data

    global TRAINED_MODEL
    if TRAINED_MODEL == None:  # Load the dumped model
        model_file = open(os.path.join(BASE_DIR, 'model.clf'), "rb")
        model = pickle.load(model_file)
        model_file.close()

    print("\n# Topic model")
    topic_model = model['topic_clf']
    topic = result_from_model(topic_model, text, 'Topic')
    final_topic = topic[0][0]

    print("\n# Intent model")
    intent_model = model['topics'][final_topic]
    intent = result_from_model(intent_model, text, 'Intent')
    final_intent = intent[0][0]
    print("\nFinal intent: %s" % final_intent)
    return {
        'final_intent': final_intent,
        'topics': topic,
        'intents': intent
    }

def run_input_test():
    user_msg = ''
    print("Type 'exit' to stop the program:")
    while not user_msg in ['exit', 'exit()']:
        user_msg = input("User message: ")
        test_model(user_msg)

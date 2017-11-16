from sklearn.pipeline import Pipeline
from .nltk_preprocessor import NLTKPreprocessor
from .w2v_model import Word2VecVectorizer
from sklearn.preprocessing import LabelEncoder
# from sklearn.ensemble import ExtraTreesClassifier
# from sklearn.linear_model import SGDClassifier
# from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

def train_model(classifier = GaussianNB()):
    raw_data = {
        'LikePets': [
            'I like dogs',
            'I like cats',
        ],
        'HatePets': [
            'I hate dogs',
            'I don\'t like dogs'
        ],
        'PetTraining': [
            'How to train my dog',
            'How to wash my cat'
        ],
        'LikeFlowers': [
            'I like sunflowers',
            'I love lilies'
        ],
        'Weather': [
            'How\'s the weather',
            'Tell me the weather'
        ]
    }

    X_train = []
    y_train = []

    for (key, value) in raw_data.items():
        for line in value:
            X_train.append(line)
            y_train.append(key)
            print('%s: %s' % (line, key))

    model = Pipeline([
        ('preprocessor', NLTKPreprocessor(stopwords=[], ignore_type=[])),
        ('vectorizer', Word2VecVectorizer(sent_size = 10)),
        # ('classifier', ExtraTreesClassifier(n_estimators=32))
        # ('classifier', SGDClassifier(loss='log'))
        # ('classifier', SVC(probability=True))
        ('classifier', classifier)
    ])

    labels = LabelEncoder()
    y_train = labels.fit_transform(y_train)

    model.labels_ = labels

    model.fit(X_train, y_train)

    while True:
        user_msg = input('Enter a command: ')

        if user_msg == 'exit':
            return

        yhat_proba = model.predict_proba([user_msg])

        labels_data = []

        for (idx, intent_proba) in enumerate(yhat_proba[0]):
            labels_data.append(
                [model.labels_.inverse_transform([idx])[0], intent_proba])

        labels_data = sorted(
            labels_data, key=lambda item: item[1], reverse=True)

        print(labels_data)
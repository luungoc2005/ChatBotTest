import numpy as np
from .nltk_pos_transformer import NLTKPreprocessor
from .w2v_padding_transformer import Word2VecVectorizer
from .text_to_array_transformer import transform_word
from sklearn.preprocessing import LabelBinarizer
import re

TOKEN_SIZE = 10

def transform_text(text, ndim=70):
    pos_transformer = NLTKPreprocessor()
    w2v_transformer = Word2VecVectorizer()
    
    # data = [text]
    data = [re.sub(' +',' ',text)]
    pos_token_data = pos_transformer.transform(data)
    # pos_token_data is in the format: array of [(token, tag)]

    w2v_data = w2v_transformer.transform(data)
    # w2v_data is in the format: array of [_w2v_array_]
    count = 0

    for sent_idx, sent in enumerate(pos_token_data):
        if len(sent) > ndim:
            print('Warning: sentence \n%s\nhas length of %s, which exceeds the limit' % (sent, str(len(sent))))
        for word_idx, word in enumerate(sent):
            # yield in the form of tag, token, w2v
            count += 1
            if count > ndim:
                raise StopIteration
            else:
                yield ( \
                    word[1], \
                    transform_word(word[0], ndim=TOKEN_SIZE), \
                    w2v_data[sent_idx][word_idx])
    while (count < ndim):
        count += 1
        # default value
        yield ( \
            '', \
            np.zeros(TOKEN_SIZE), \
            np.zeros(w2v_transformer.dim))

# def force_dim(array, ndim=50):
#     if len(array) == ndim:
#         return array
#     elif len(array) > ndim:
#         return array[0:ndim]
#     else:
#         return np.pad(array, (0, ndim-len(array)), 'constant')

def transform_examples(text_array):
    pos_input = []
    char_input = []
    w2v_input = []
    pos_tag_list = []

    for text in text_array:
        line_pos = []
        line_char = []
        line_w2v = []
        for data_point in list(transform_text(text)):
            line_pos.append(data_point[0]) #tag
            line_char.append(data_point[1]) #token
            line_w2v.append(data_point[2]) #w2v
            pos_tag_list.append(data_point[0])
        pos_input.append(line_pos)
        char_input.append(line_char)
        w2v_input.append(line_w2v)
    
    pos_labels = LabelBinarizer()
    pos_labels.fit(pos_tag_list)

    pos_input = [
        pos_labels.transform(X) for X in pos_input
    ]

    return {
        'pos_input': pos_input,
        'char_input': char_input,
        'w2v_input': w2v_input,
        '_pos_labels': pos_labels
    }

# With input_data in the form of (example, intent)
def transform_train_input(input_data):
    X_train = []
    Y_train = []

    for example, intent in input_data:
        X_train.append(example)
        Y_train.append(intent)
    
    # Transform Y_train
    labels = LabelBinarizer()
    Y_train = np.array(labels.fit_transform(Y_train)).astype('float32')

    # Transform X_train
    X_transform = transform_examples(X_train)
    X_char = np.array(np.concatenate( \
        (X_transform['pos_input'], \
        X_transform['char_input']), \
        axis=2)).astype('float32')
    X_w2v = np.array(np.concatenate( \
        (X_transform['pos_input'], \
        X_transform['w2v_input']), \
        axis=2)).astype('float32')
    
    return {
        'X_char': X_char,
        'X_w2v': X_w2v,
        'Y_train': Y_train,
        '_labels': labels,
        '_pos_labels': X_transform['_pos_labels']
    }

def transform_X_input(text, data_model):
    # Extract tag, token, w2v info
    pos_input = []
    char_input = []
    w2v_input = []
    pos_labels = data_model['_pos_labels']

    for data_point in list(transform_text(text)):
        pos_input.append(data_point[0]) #tag
        char_input.append(data_point[1]) #token
        w2v_input.append(data_point[2]) #w2v
    
    pos_input = pos_labels.transform(pos_input)

    X_char = np.array([np.concatenate( \
        (pos_input, \
        char_input), \
        axis=1)]).astype('float32')
    X_w2v = np.array([np.concatenate( \
        (pos_input, \
        w2v_input), \
        axis=1)]).astype('float32')
    
    return {
        'X_char': X_char,
        'X_w2v': X_w2v
    }
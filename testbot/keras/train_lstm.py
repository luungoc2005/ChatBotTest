# Training details. We train 2-layer LSTMs of 512 units with bidirectional encoder (i.e., 1 bidirectional layers for the encoder), embedding dim is 512. LuongAttention (scale=True) is used together with dropout keep_prob of 0.8. All parameters are uniformly. We use SGD with learning rate 1.0 as follows: train for 12K steps (~ 12 epochs); after 8K steps, we start halving learning rate every 1K step.
import pickle
from keras.backend import argmax
from keras.layers import Input, LSTM, Dense, Dropout, concatenate
from keras.models import Model, model_from_json
from keras.utils import to_categorical
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from keras import regularizers

from .data_lstm import *
from .test_data import *
from ..models import Example

FILE_PATH='models/weights-{epoch:02d}-{loss:.4f}.h5'
ARCH_PATH='models/model.json'
WEIGHTS_PATH = 'models/model.h5'
DATA_PATH = 'models/model.pickle'

def build_model():
    data = [
        (item.text, item.intent.name) 
        for item in list(Example.objects.all())
    ]

    data = transform_train_input(data)

    # return {
    #     'X_char': X_char,
    #     'X_w2v': X_w2v,
    #     'Y_train': Y_train,
    #     '_labels': labels,
    #     '_pos_labels': X_transform['_pos_labels']
    # }
    X_char = data['X_char']
    X_w2v = data['X_w2v']
    Y_train = data['Y_train']
    classes = len(data['_labels'].classes_)
    with open(DATA_PATH, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

    input_chr = Input(shape=(X_char.shape[1], X_char.shape[2]), dtype='float32', name='chr_input')
    lstm_chr = LSTM(6)(input_chr)
    lstm_chr = Dropout(0.2)(lstm_chr)
    output_chr = Dense(classes, activation='sigmoid', name='chr_output')(lstm_chr)

    input_w2v = Input(shape=(X_w2v.shape[1], X_w2v.shape[2]), dtype='float32', name='w2v_input')
    lstm_w2v = LSTM(32)(input_w2v)
    lstm_w2v = Dropout(0.2)(lstm_w2v)
    output_w2v = Dense(classes, activation='sigmoid', name='w2v_output')(lstm_w2v)

    x = concatenate([lstm_chr, lstm_w2v])
    x = Dense(16, activation='relu')(x)
    x = Dropout(0.5)(x)

    main_output = Dense(classes, activation='sigmoid', name='main_output')(x)

    model = Model(inputs=[input_chr, input_w2v], outputs=[main_output, output_chr, output_w2v])
    model.compile(optimizer='nadam', 
        loss='binary_crossentropy', 
        loss_weights={'main_output': 0.5, 'chr_output': 0.2, 'w2v_output': 0.3})

    callbacks = [
        TensorBoard(log_dir='./logs'),
        ModelCheckpoint(FILE_PATH, 
            monitor='loss', 
            verbose=1, 
            save_best_only=True, 
            mode='min',
            period=500),
        EarlyStopping(monitor='loss', 
            min_delta=0.0001, 
            patience=500, 
            verbose=1, 
            mode='auto')
    ]

    with open(ARCH_PATH, 'w') as model_arch:
        model_arch.write(model.to_json())

    batch_size = max([len(X_char), 16])

    model.fit([X_char, X_w2v], [Y_train, Y_train, Y_train], 
        epochs=10000, 
        batch_size=batch_size,
        callbacks=callbacks)

    model.save_weights(WEIGHTS_PATH)

DATA_OBJ = None
MODEL_OBJ = None

def load_model(input_model=None):
    global DATA_OBJ, MODEL_OBJ

    if not DATA_OBJ or not MODEL_OBJ:
        with open(DATA_PATH, 'rb') as pickle_file:
            data = pickle.load(pickle_file)

        with open(ARCH_PATH, 'r') as model_arch:
            model = model_from_json(model_arch.read())
        
        if not input_model:
            model.load_weights(WEIGHTS_PATH)
        else:
            model.load_weights(input_model)

        DATA_OBJ = data
        MODEL_OBJ = model
    else:
        data = DATA_OBJ
        model = MODEL_OBJ

        if input_model:
            model.load_weights(input_model)

    return (data, model)

def test_model(text, input_model=None):
    data, model = load_model(input_model=input_model)
    X_input = transform_X_input(text, data)
    
    result = model.predict([X_input['X_char'], X_input['X_w2v']], 
        batch_size=1, 
        verbose=0)

    max_point = result[0][0].argmax()
    sum_proba = sum(result[0][0])
    sum_chars_proba = sum(result[1][0])
    sum_w2v_proba = sum(result[2][0])

    proba = result[0][0][max_point] / sum_proba * 100
    chars_proba = result[1][0][max_point] / sum_chars_proba * 100
    w2v_proba = result[2][0][max_point] / sum_w2v_proba * 100

    print((data['_labels'].classes_[max_point], proba, chars_proba, w2v_proba))

    return result
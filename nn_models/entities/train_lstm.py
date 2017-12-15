# Training details. We train 2-layer LSTMs of 512 units with bidirectional encoder (i.e., 1 bidirectional layers for the encoder), embedding dim is 512. LuongAttention (scale=True) is used together with dropout keep_prob of 0.8. All parameters are uniformly. We use SGD with learning rate 1.0 as follows: train for 12K steps (~ 12 epochs); after 8K steps, we start halving learning rate every 1K step.
import pickle
from keras.backend import argmax
from keras.layers import Input, LSTM, Bidirectional, Dense, Dropout, concatenate
from keras.layers.wrappers import TimeDistributed
from keras.models import Model, model_from_json
from keras.utils import to_categorical
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from keras import regularizers

from nn_models.preprocessing.data_entities import *
from nn_models.preprocessing.test_data import *
# from ..models import Example

FILE_PATH='models/entities/weights-{epoch:02d}-{loss:.4f}.h5'
ARCH_PATH='models/entities/model.json'
WEIGHTS_PATH = 'models/entities/model.h5'
DATA_PATH = 'models/entities/model.pickle'

RECURRENT_DEPTH = 3
RECURRENT_UNITS = 128

def build_model():
    # data = [
    #     (item.text, item.intent.name) 
    #     for item in list(Example.objects.all())
    # ]
    data = list(entities_to_list(test_entities_animals))
    # data = list(to_list(test_data_likes))
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
    classes = Y_train.shape[2]

    print('Data statistics:')
    print('Character inputs matrix has shape %s' % str(X_char.shape))
    print('GloVE input matrix has shape %s' % str(X_w2v.shape))
    print('Target classes has shape %s' % str(Y_train.shape))
    print('Number of classes: %s' % classes)

    with open(DATA_PATH, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)
    
    input_chr = Input(shape=(X_char.shape[1], X_char.shape[2]), dtype='float32', name='chr_input')
    input_w2v = Input(shape=(X_w2v.shape[1], X_w2v.shape[2]), dtype='float32', name='w2v_input')

    conv_chr = FILTER_SIZES[:]
    conv_w2v = FILTER_SIZES[:]

    NUM_FILTERS = len(FILTER_SIZES)
    for idx, _ in enumerate(RECURRENT_DEPTH):
        conv_chr[idx] = Bidirectional(LSTM(RECURRENT_UNITS, return_sequences=True))(input_chr if idx == 0 else conv_chr[idx-1])
        conv_chr[idx] = Dropout(0.5)(conv_chr[idx])
        # conv_chr[i] = Flatten()(conv_chr[i])
        # output_chr = Dense(classes, activation='sigmoid', name='chr_output')(lstm_chr)

        conv_w2v[idx] = Bidirectional(LSTM(RECURRENT_UNITS, return_sequences=True))(input_w2v if idx == 0 else conv_w2v[idx-1])
        conv_w2v[idx] = Dropout(0.5)(conv_w2v[idx])
        # conv_w2v[i] = Flatten()(conv_w2v[i])
        # output_w2v = Dense(classes, activation='sigmoid', name='w2v_output')(lstm_w2v)

    output_chr = TimeDistributed(Dense(classes, activation='softmax', name='chr_output'))(conv_chr[RECURRENT_DEPTH - 1])

    output_w2v = TimeDistributed(Dense(classes, activation='softmax', name='w2v_output'))(conv_w2v[RECURRENT_DEPTH - 1])
    
    x = concatenate([conv_chr, conv_w2v])

    main_output = TimeDistributed(Dense(classes, activation='softmax', name='main_output'))(x)

    model = Model(inputs=[input_chr, input_w2v], outputs=[main_output, output_chr, output_w2v])
    model.compile(optimizer='adam', 
        loss='categorical_crossentropy',
        loss_weights={'main_output': 0.5, 'chr_output': 0.3, 'w2v_output': 0.2},
        metrics=['accuracy'])

    batch_size = min([len(X_char), 16])

    callbacks = [
        TensorBoard(log_dir='./logs/entities',
            write_graph=True,
            write_images=True, 
            write_grads=True,
            batch_size=batch_size),
        ModelCheckpoint(FILE_PATH, 
            monitor='loss', 
            verbose=1, 
            save_best_only=True, 
            mode='min',
            period=20),
        EarlyStopping(monitor='loss', 
            min_delta=0.0001, 
            patience=200, 
            verbose=1, 
            mode='auto')
    ]

    with open(ARCH_PATH, 'w') as model_arch:
        model_arch.write(model.to_json())

    try:
        model.fit([X_char, X_w2v], [Y_train, Y_train, Y_train], 
            epochs=5000, 
            batch_size=batch_size,
            callbacks=callbacks,
            shuffle=True)

        model.save_weights(WEIGHTS_PATH)
    except KeyboardInterrupt:
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

    return result
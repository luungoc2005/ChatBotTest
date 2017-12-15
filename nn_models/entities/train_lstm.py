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
from nn_models.preprocessing.nltk_pos_transformer import *
# from ..models import Example

FILE_PATH='models/entities/weights-{epoch:02d}-{loss:.4f}.h5'
ARCH_PATH='models/entities/model.json'
WEIGHTS_PATH = 'models/entities/model.h5'
DATA_PATH = 'models/entities/model.pickle'

RECURRENT_DEPTH = 2
RECURRENT_UNITS = 32

def build_model():
    # data = [
    #     (item.text, item.intent.name) 
    #     for item in list(Example.objects.all())
    # ]
    data = list(entities_to_list(test_entities))
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

    conv_chr = list(range(RECURRENT_DEPTH))
    conv_w2v = list(range(RECURRENT_DEPTH))

    for idx in range(RECURRENT_DEPTH):
        conv_chr[idx] = Dropout(0.3)(input_chr if idx == 0 else conv_chr[idx-1])
        conv_chr[idx] = Bidirectional(LSTM(RECURRENT_UNITS, return_sequences=True))(conv_chr[idx])
        conv_chr[idx] = Dropout(0.5)(conv_chr[idx])

        conv_w2v[idx] = Dropout(0.3)(input_w2v if idx == 0 else conv_w2v[idx-1])
        conv_w2v[idx] = Bidirectional(LSTM(RECURRENT_UNITS, return_sequences=True))(conv_w2v[idx])
        conv_w2v[idx] = Dropout(0.5)(conv_w2v[idx])

    output_chr = TimeDistributed(Dense(classes, activation='softmax'), name='chr_output')(conv_chr[RECURRENT_DEPTH - 1])

    output_w2v = TimeDistributed(Dense(classes, activation='softmax'), name='w2v_output')(conv_w2v[RECURRENT_DEPTH - 1])
    
    x = concatenate([conv_chr[-1], conv_w2v[-1]])

    main_output = TimeDistributed(Dense(classes, activation='softmax'), name='main_output')(x)

    model = Model(inputs=[input_chr, input_w2v], outputs=[main_output, output_chr, output_w2v])
    model.compile(optimizer='adam', 
        loss='categorical_crossentropy',
        loss_weights={'main_output': 0.5, 'chr_output': 0.3, 'w2v_output': 0.2},
        metrics=['categorical_accuracy'])

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
    nltk_transformer = NLTKPreprocessor(mutate=False)

    X_input = transform_X_input(text, data)
    X_pos = nltk_transformer.transform([text])[0]

    text_result = []
    
    result = model.predict([X_input['X_char'], X_input['X_w2v']], 
        batch_size=1, 
        verbose=0)

    for idx, (token, tag) in enumerate(X_pos):
        if result[0][0][idx][0] > 0.5:
            text_result.append((token, result[0][0][idx][0] * 100, result[0][0][idx][1] * 100))

    entity_text = ' '.join([text for (text, acc1, acc2) in text_result])
    accuracy = np.mean([acc1 for (text, acc1, acc2) in text_result])

    return text_result
import numpy as np

def transform_word(word, ndim=10):
    result = list([
        ord(char) / 255
        for char in word[0:ndim]
    ])
    if len(result) == ndim:
        return np.array(result, dtype='float32')
    else:
        return np.array( \
            np.pad(result, (0, ndim-len(result)), 'constant'))
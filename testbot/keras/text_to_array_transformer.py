import numpy as np

def transform_word(word, ndim=10):
    result = list([
        ord(char)
        for char in word[0:ndim-1]
    ])
    if len(result) == ndim:
        return np.array(result, dtype='float16')
    else:
        return np.array( \
            np.pad(result, (0, ndim-len(result)), 'constant'))
test_data_lights = {
    'TurnOff': [
        'Turn off that light',
        'Turn off this lamp'
    ],
    'TurnOn': [
        'Turn the lamp on',
        'Light, on'
    ],
    'TurnMultipleOn': [
        'Turn the lights on',
        'Lamps on'
    ],
    'TurnMultipleOff': [
        'Turn that lamp off',
        'Turn off the lights'
    ]
}

test_data_likes = {
    'LikeAnimals': [
        'I like cats',
        'I like my dog',
        'My favorite are mice'
    ],
    'LikeFlowers': [
        'I like sunflowers',
        'My favorite must be lilies'
    ]
}

def to_list(test_data):
    for key in test_data.keys():
        for sent in test_data[key]:
            yield (sent, key)
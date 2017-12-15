import json

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

test_entities = [
    ('my email is luungoc2005@yahoo.com', (3, 7)),
    ('email: no.name01@yahoo.com', (2,8)),
    ('email me at: asdf@gmail.com', (2,8)),
    ('contact us at contact@microsoft.com and we will get back to you', (3, 7))
]

test_entities_animals = [
    ('my favorite animals are sloths', (4, 4)),
    ('I like cats', (2, 2)),
    ('I like to keep a pet fox at home', (6, 6)),
]

def to_list(test_data):
    for key in test_data.keys():
        for sent in test_data[key]:
            yield (sent, key)

def entities_to_list(test_data, ndim = 70):
    for text, (start, end) in test_data:
        result_arr = [[1.0, 0.0] if x >= start and x <= end else [0.0, 1.0]
            for x in range(ndim)]
        yield (text, result_arr)

def load_from_json(JSON_FILE):
    data = {}
    with open(JSON_FILE, errors='ignore') as json_file:
        json_data = json.load(json_file)
    for intent_object in json_data:
        if not data.get(intent_object['name'], None):
            data[intent_object['name']] = []
        for example in intent_object['usersays']:
            data[intent_object['name']].append(example.strip())
    return data
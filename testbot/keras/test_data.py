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

def to_list(test_data):
    for key in test_data.keys():
        for sent in test_data[key]:
            yield (sent, key)

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
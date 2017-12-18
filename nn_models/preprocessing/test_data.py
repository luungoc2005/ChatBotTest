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

test_data_mindmeld = {
    'GREETING': [
        'Hi',
        'Hello',
        'Hola',
        'Good morning'
    ],
    'CLOSING': [
        'Ciao',
        'Bye',
        'See you!'
    ],
    'AFFIRMATIVE': [
        'OK',
        'Yes please',
        'Yep'
    ],
    'NEGATIVE': [
        'Nope',
        'No not this one but the first one',
        'No'
    ],
    'ORDER': [
        'A medium soy milk latte with hazelnut and caramel syrups and two slices of lemon bread.',
        'A grande java chip frappuccino with nonfat milk, an iced coffee with skim milk and one shot of vanilla syrup and a bottle of water.',
        'I would like a small americano with room for cream and large drip coffee, black.',
        'I want a venti blonde roast, room for cream, a blueberry scone and a grande shaken sweet tea lemonade.',
        'Can I please have a bacon cheddar breakfast sandwich and large cappuccino?',
        'I\'ll have a grande iced caramel macchiato with an extra shot and a tall iced green tea latte, a tall chai tea and a grande latte.',
        'Can i get a regular small coffee with no sugar and a blueberry muffin?',
        'I would like a double upside down macchiato half decaf with room and a splash of cream in a grande cup.',
        'I\'ll take a tall frappuccino with two scoops of vanilla bean powder and caramel drizzle.',
        'How about a venti caramel frappuccino with extra mocha drizzle and a raspberry scone?',
        'Give me ten pieces of pumpkin cake and a pike place coffee traveler.',
        'I would like to order a venti white chocolate frappuccino with heavy mocha drizzle, soy milk and extra ice.',
        'I want a nonfat mocha, no whip, and two pumpkin scones.',
        'Can I place an order for a tall coffee with cream and sugar and a pumpkin spice latte with nutmeg?',
        'One grande cappucino with vanilla syrup and sugar and a short green tea.',
        'Can I get a tall mocha frappucino as well as a chocolate croissant?',
        'Give me your largest vanilla latte with light whipped cream and a ham and cheese sandwich.',
        'Could I please have a large hot chocolate with whip and a cinnamon chip scone?',
        'Can I have an iced mocha made with coconut milk with extra whipped cream and a drizzle of caramel on it and a bottle of water?',
        'I\'ll take a small frappuccino with two scoops of vanilla bean powder, honey and caramel drizzle.',
        'I need a large cinnamon dolce latte with nonfat milk, no whip and an extra shot and a slice of pumpkin cake.',
        'Can I have three large decaf coffees and three almond croissants?',
    ],
    'COMPLIMENT': [
        'You are the best personal assistant.'
    ]
}

test_entities = [
    ('my email is luungoc2005@yahoo.com', (3, 7)),
    ('email: no.name01@yahoo.com', (2,8)),
    ('email me at: asdf@gmail.net', (2,8)),
    ('contact us at contact@microsoft.org and we will get back to you', (3, 7))
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
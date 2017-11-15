from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Intent, Example
from .transform import tokenize_text, test_transform
import json
# Create your views here.


def index(request):
    response = {
        'intents': []
    }
    for intent in Intent.objects.all():
        new_intent = {
            'name': intent.name,
            'examples': [example.text for example in intent.example_set.all()]
        }
        response['intents'].append(new_intent)

    print(response)
    return render(request, 'index.html', response)


def examples(request):
    custom_query = request.GET.get('query')

    response = {
        'examples': []
    }
    
    if request.content_type == 'application/json':
        if custom_query == None:
            for example in Example.objects.all():
                new_example = {
                    'text': example.text,
                    'result': tokenize_text(example.text)
                }
                response['examples'].append(new_example)
        else:
            response['examples'].append({
                'text': custom_query,
                'result': tokenize_text(custom_query)
            })
        return JsonResponse(response)
    else:
        if custom_query == None:
            for example in Example.objects.all():
                new_example = {
                    'text': example.text,
                    'result': json.dumps(tokenize_text(example.text), sort_keys=True, indent=4)
                }
                response['examples'].append(new_example)
        else:
            response['examples'].append({
                'text': custom_query,
                'result': json.dumps(tokenize_text(custom_query), sort_keys=True, indent=4)
            })
        return render(request, 'examples.html', response)


def test(request):
    examples = list(Example.objects.all())
    response = {
        'data': test_transform([example.text for example in examples]),
        'size': len(examples)
    }
    return render(request, 'test.html', response)

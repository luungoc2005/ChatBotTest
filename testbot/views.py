from django.shortcuts import render
from django.http import HttpResponse
from .models import Intent, Example

from .transform import tokenize_text

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

  if custom_query == None:
    for example in Example.objects.all():
      new_example = {
        'text': example.text,
        'transform': tokenize_text(example.text)
      }
      response['examples'].append(new_example)
  else:
    response['examples'].append({
      'text': custom_query,
      'transform': tokenize_text(custom_query)
    })
  return render(request, 'examples.html', response)
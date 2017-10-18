from django.urls import path

from . import views

urlpatterns = [
    # ex: /testbot/
    path('', views.index, name='index'),
    path('examples/', views.examples, name='examples'),
    path('test/', views.test, name='test'),
]
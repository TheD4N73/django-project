from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'recipes/pages/index.html')


def recipes(request, id):
    return render(request, 'recipes/pages/recipe-view.html')

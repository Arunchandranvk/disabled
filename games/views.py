from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class Main(TemplateView):
    template_name='index.html'

class GuessTheAnimal(TemplateView):
    template_name='GuessTheAnimal.html'

class Math(TemplateView):
    template_name='maths.html'

class Memory(TemplateView):
    template_name='memory.html'



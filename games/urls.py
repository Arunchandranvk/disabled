from django.urls import path
from .views import *

urlpatterns = [
    path('activities/',Main.as_view(),name='game'),
    path('guesstheanimal/',GuessTheAnimal.as_view(),name='animal'),
    path('math/',Math.as_view(),name='math'),
    path('memory/',Memory.as_view(),name='memory'),
]
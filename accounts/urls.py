from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login_faculty/',LoginViewFaculty.as_view(),name='login'),
    path('login_student/',face_login_view,name='face_login'),
    path('suggestion-Create/',SuggTextView.as_view(),name='sug-add'),
    path('suggestion/',SugView.as_view(),name='suggestions'),
    path('delsug/<int:pk>/',DeleteViewSug.as_view(),name='sdel'),
    path('cphome/',ChangePasswordViewHome.as_view(),name="chp"),
    path('sugupdate/<int:pk>/',SuggestionUpdateView.as_view(),name='supd'),
    path('dataclear/',ClearDataView.as_view(),name='cl')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)           
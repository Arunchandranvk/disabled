from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('shome/',StuHomeView.as_view(),name="sh"),
    path('ex/',studentanswer,name='ans'),
    path('eximg/',studentanswer_image,name='ansimg'),
    path('exaudio/',studentanswer_audio,name='ansaudio'),
    path('submit/',submit_exam,name='submit_exam'),
    path('submitaudio/',submit_exam_audio,name='submit_examaudio'),
    path('submitimage/',submit_exam_image,name='submit_examimage'),
    path('profile/',Profile.as_view(),name='pro'),
    path('sug/',SugView.as_view(),name='sug'),
    path('result/<int:pk>/',ResultView.as_view(),name='res'),
    path('cp/',ChangePasswordView.as_view(),name="cp"),
    path('logout/',LogOut.as_view(),name="logout"),
    path('proupdate/<int:pk>/',ProfileUpdateView.as_view(),name="proupd"),
    path('video/',Text.as_view(),name='text'),
    path('audio/',Audio.as_view(),name='audio'),
    path('noteview/<int:pk>/',NotesListView.as_view(),name='noteview'),
    path('voice-recogonization/',voice_recognition,name='voice'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('bot/',ChatBotView.as_view(),name='bot'),
    path('messagesview',MessageGetView.as_view(),name='msgview'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
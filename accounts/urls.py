from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('addd/',AddStudent.as_view(),name='add'),
    path('quest/<int:pk>/',QuestView.as_view(),name='que'),
    path('test/<int:pk>/',Test,name='tt'),
    path('assign/',AssignView,name='testall'),
    path('assignvisual/',AssignImageView,name='testallvisual'),
    path('assignhear/',AssignAudioView,name='testallhear'),
    path('qansupd/',QuesAnsUpdView.as_view(),name='qans'),
    path('qansimg/',QuesAnsImageView.as_view(),name='qansimg'),
    path('qansaudio/',QuesAnsAudioView.as_view(),name='qansaudio'),
    path('del/<int:pk>/',DeleteView.as_view(),name='dq'),
    path('delimg/<int:pk>/',DeleteImgView.as_view(),name='dqimg'),
    path('delaudio/<int:pk>/',DeleteAudioView.as_view(),name='dqaudio'),
    path('questionadd/',Quesadd.as_view(),name="qdel"),
    path('questionimg/',Quesimage.as_view(),name="qimg"),
    path('questionaudio/',Quesaudio.as_view(),name="qaudio"),
    path('suggestiontext/',SuggTextView.as_view(),name='st'),
    path('suggestionvideo/',SuggVideoView.as_view(),name='sv'),
    path('suggestionaudio/',SuggAudioView.as_view(),name='sa'),
    path('suggestion/',SugView.as_view(),name='sadd'),
    path('video/<int:video_id>/', views.view_video, name='view_video'),
    path('videoo/<int:videoo_id>/', views.view_videoo, name='view_videoo'),
    path('audio/<int:audio_id>/', views.play_audio, name='play_audio'),
    path('audioo/<int:audio_id>/', views.play_audioo, name='play_audioo'),
    path('delsug/<int:pk>/',DeleteViewSug.as_view(),name='sdel'),
    path('cphome/',ChangePasswordViewHome.as_view(),name="chp"),
    path('sugupdate/<int:pk>/',SuggestionUpdateView.as_view(),name='supd'),
    path('questionupdate/<int:pk>/',QuesUpdate.as_view(),name='qupd'),
    path('dataclear/',ClearDataView.as_view(),name='cl')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
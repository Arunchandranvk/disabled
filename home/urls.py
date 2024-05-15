from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mainhome/',HomeView.as_view(),name='h'),
    path('students/',StudentsView.as_view(),name='stu'),
    path('search/',Search.as_view(),name="sea"),
    path('detail/<int:pk>/',DetailView.as_view(),name='det'),
    path('Test_details/',Score_view.as_view(),name='score'),
    path('qhome/',Ques.as_view(),name="q"),
    path('sd/<int:pk>/',SD.as_view(),name='sd'),
    path('notes/',NotesView.as_view(),name='note'),
    path('del/<int:pk>/',DeleteViewNotes.as_view(),name='d'),
    path('deldetails/<int:pk>/',DeleteViewExamDetails.as_view(),name='deldet'),
    path('deldetailsaudio/<int:pk>/',DeleteViewExamDetailsAudio.as_view(),name='delaudio'),
    path('messages',MessageView.as_view(),name='msg'),
    path('viewedusers/<int:pk>/',MsgViewed.as_view(),name='v_msg')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
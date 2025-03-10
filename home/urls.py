from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mainhome/',HomeView.as_view(),name='h'),
    path('students/',StudentsView.as_view(),name='stu'),
    path('search/',Search.as_view(),name="sea"),
    path('detail/<int:pk>/',DetailView.as_view(),name='det'),
    path('questions/<int:pk>/',Questionadd.as_view(),name="question"),
    path('exams/',ExamCreate.as_view(),name="exam-name"),
    path('update-question/<int:pk>/',QuestionUpdateView.as_view(),name="update-ques"),
    path('delete-question/<int:question_id>/',QuestionDeleteView,name="del-ques"),
    path('delete-exam/<int:exam_id>/',ExamDeleteView,name="del-exam"),
    path('notes/',NotesView.as_view(),name='note'),
    path('del/<int:pk>/',DeleteViewNotes.as_view(),name='d'),
    path('exam-details/',ExamDetailsview.as_view(),name='exam-detail'),
    path('exam-details-student/<int:pk>/',StudentExamDetailsview.as_view(),name='exam-detail-student'),
    path('assign-exam/<int:exam_id>/',AssignExamView,name='assign-exam'),
    path('deactivate-exam/<int:exam_id>/',DeactivateExamView,name='deactivate-exam'),
    path('messages',MessageView.as_view(),name='msg'),
    path('viewedusers/<int:pk>/',MsgViewed.as_view(),name='v_msg')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
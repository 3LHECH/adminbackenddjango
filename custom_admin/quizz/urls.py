from django.urls import path
from . import views

urlpatterns = [
    path('quizz/', views.QuizzListView.as_view(), name='quizz_list'),
    path('quizz/<int:pk>/', views.QuizzDetailView.as_view(), name='quizz_detail'),
    path('quizz/create/', views.QuizzCreateView.as_view(), name='quizz_create'),
    path('quizz/<int:pk>/update/', views.QuizzUpdateView.as_view(), name='quizz_update'),
    path('quizz/<int:pk>/delete/', views.QuizzDeleteView.as_view(), name='quizz_delete'),
    path('api/quizz_chart/', views.quizz_chart, name='quizz_chart'),

    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('api/question_chart/', views.question_chart, name='question_chart'),

    path('answers/', views.AnswerListView.as_view(), name='answer_list'),
    path('answer/<int:pk>/', views.AnswerDetailView.as_view(), name='answer_detail'),
    path('answer/create/', views.AnswerCreateView.as_view(), name='answer_create'),
    path('answer/<int:pk>/update/', views.AnswerUpdateView.as_view(), name='answer_update'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='answer_delete'),
    path('api/correct_answer/', views.correct_answer_chart, name='correct_answer'),
    path('api/wrong_answer/', views.wrong_answer_chart, name='wrong_answer'),


]

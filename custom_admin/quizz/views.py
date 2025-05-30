from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quizz, Question, Answer
from .forms import QuizzForm, QuestionForm, AnswerForm
from django.utils.timezone import now, timedelta
from rest_framework.decorators import api_view
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.response import Response
from django.contrib import messages
from user.models import User
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsStaff,StaffRequiredMixin
class QuizzListView(LoginRequiredMixin,StaffRequiredMixin, ListView):
    model = Quizz
    context_object_name = 'quizzes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = now()
        start_of_this_week = today - timedelta(days=7)
        start_of_last_week = today - timedelta(days=14)

        new_quizzs_this_week = Quizz.objects.filter(created_at__gte=start_of_this_week).count()

        new_quizzs_last_week = Quizz.objects.filter(
            created_at__gte=start_of_last_week,
            created_at__lt=start_of_this_week
        ).count()

        if new_quizzs_last_week == 0:
            if new_quizzs_this_week == 0:
                percent_change = 0
            else:
                percent_change = 100 
        else:
            percent_change = ((new_quizzs_this_week - new_quizzs_last_week) / new_quizzs_last_week) * 100

        context['new_quizzs_this_week'] = new_quizzs_this_week
        context['new_quizzs_last_week'] = new_quizzs_last_week
        context['percent_change'] = round(percent_change, 2)
        return context


@api_view(['GET'])
def quizz_chart(request):
    data = (
        Quizz.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    return Response(data)

class QuizzDetailView(LoginRequiredMixin,StaffRequiredMixin, DetailView):
    model = Quizz
    template_name = 'quizz/quizz_detail.html'

class QuizzCreateView(LoginRequiredMixin,StaffRequiredMixin, CreateView):
    model = Quizz
    form_class = QuizzForm
    template_name = 'quizz/quizz_create.html'
    success_url = reverse_lazy('quizz_list')


class QuizzUpdateView(LoginRequiredMixin,StaffRequiredMixin, UpdateView):
    model = Quizz
    form_class = QuizzForm
    success_url = reverse_lazy('quizz_list')
    template_name = 'quizz/quizz_update.html'


class QuizzDeleteView(LoginRequiredMixin,StaffRequiredMixin, DeleteView):
    model = Quizz
    success_url = reverse_lazy('quizz_list')


class QuestionListView(LoginRequiredMixin,StaffRequiredMixin, ListView):
    model = Question
    template_name = 'quizz/question_list.html'
    context_object_name = 'questions'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = now()
        start_of_this_week = today - timedelta(days=7)
        start_of_last_week = today - timedelta(days=14)

        new_question_this_week = Question.objects.filter(created_at__gte=start_of_this_week).count()

        new_question_last_week = Question.objects.filter(
            created_at__gte=start_of_last_week,
            created_at__lt=start_of_this_week
        ).count()

        if new_question_last_week == 0:
            if new_question_this_week == 0:
                percent_change = 0
            else:
                percent_change = 100 
        else:
            percent_change = ((new_question_this_week - new_question_last_week) / new_question_last_week) * 100

        context['new_question_this_week'] = new_question_this_week
        context['new_question_last_week'] = new_question_last_week
        context['percent_change'] = round(percent_change, 2)
        return context


@api_view(['GET'])
@permission_classes([IsStaff])
def question_chart(request):
    data = (
        Question.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    return Response(data)

class QuestionDetailView(LoginRequiredMixin,StaffRequiredMixin, DetailView):
    model = Question
    template_name = 'quizz/question_detail.html'

class QuestionCreateView(LoginRequiredMixin,StaffRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quizz/question_create.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your question has been saved!')
        return response
    
class QuestionUpdateView(LoginRequiredMixin,StaffRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('question_list')
    template_name = 'quizz/question_update.html'

class QuestionDeleteView(LoginRequiredMixin,StaffRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('question_list')

@api_view(['GET'])
@permission_classes([IsStaff])
def question_chart(request):
    data = (
        Question.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    return Response(data)

class AnswerListView(LoginRequiredMixin,StaffRequiredMixin, ListView):
    model = Answer
    context_object_name = 'answers'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['user_to_see_answears'] = User.objects.all()

        return context

class AnswerDetailView(LoginRequiredMixin,StaffRequiredMixin, DetailView):
    model = Answer
    template_name = 'quizz/answer_detail.html'

class AnswerCreateView(LoginRequiredMixin,StaffRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    success_url = reverse_lazy('answer_list')
    template_name = 'quizz/answer_create.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Your Answear has been saved!')
        return super().form_valid(form)

class AnswerUpdateView(LoginRequiredMixin,StaffRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    success_url = reverse_lazy('answer_list')
    template_name = 'quizz/answer_update.html'

class AnswerDeleteView(LoginRequiredMixin,StaffRequiredMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy('answer_list')

@api_view(['GET'])
@permission_classes([IsStaff])
def correct_answer_chart(request):
    email = request.GET.get('email')
    answers = Answer.objects.filter(is_correct=True)

    if email:
        answers = answers.filter(user__email=email)

    result = (
        answers
        .annotate(month=TruncMonth('answered_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    data = list(result)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsStaff])
def wrong_answer_chart(request):
    email = request.GET.get('email')
    answers = Answer.objects.filter(is_correct=False)
    print(email)
    if email:
        answers = answers.filter(user__email=email)

    result = (
        answers
        .annotate(month=TruncMonth('answered_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    data = list(result)
    return Response(data)



from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm ,CustomUserLogin,UserUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model 
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User
from .forms import UserUpdateForm 
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.utils.timezone import now, timedelta
from .permissions import IsStaff,StaffRequiredMixin
from quizz.models import Question,Answer
from django.db.models import Count, Q

User = get_user_model()
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = UserUpdateForm(instance=request.user)

        QUESTION_TYPE_LABELS = {
            'DS': 'Data Science',
            'IOT': 'Internet of Things',
            'CL': 'Cloud Computing',
            'GL': 'Genie Logiciel',
        }

        stats = (
            Answer.objects
            .filter(user=request.user)
            .values('question__type')
            .annotate(
                total=Count('id'),
                correct=Count('id', filter=Q(is_correct=True))
            )
        )

        score_by_type = {}
        for item in stats:
            q_type = item['question__type']
            total = item['total']
            correct = item['correct']
            percent = (correct / total) * 100 if total > 0 else 0
            label = QUESTION_TYPE_LABELS.get(q_type, q_type)  # convert code to label
            score_by_type[label] = round(percent, 2)

        return render(
            request,
            "user/profile.html",
            {
                'form': form,
                'score_by_type': score_by_type
            }
        )
    else:
        form_login = CustomUserLogin()
        return render(request, "user/login.html", {"form_login": form_login})
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return redirect('profile')  
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(request.META.get('HTTP_REFERER', '/'))



def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field][0])
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('home')

def logout_user(request):
    if(logout(request)):
        return redirect('home')
    return redirect('home')

@login_required

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if request.htmx:
                profile_html = render_to_string('user/partials/profile_summary.html', {'user': user})
                form_html = render_to_string('user/partials/profile_form.html', {'form': form})
                return HttpResponse(profile_html + form_html)
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    if request.htmx:
        form_html = render_to_string('user/partials/profile_form.html', {'form': form})
        return HttpResponse(form_html)

    return render(request, 'user/profile.html', {'form': form})


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('home')  
        

class UserListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = User
    template_name = 'user/user_list.html'  
    context_object_name = 'users'
    ordering = ['first_name']  
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = now()
        start_of_this_week = today - timedelta(days=7)
        start_of_last_week = today - timedelta(days=14)

        new_users_this_week = User.objects.filter(created_at__gte=start_of_this_week).count()

        new_users_last_week = User.objects.filter(
            created_at__gte=start_of_last_week,
            created_at__lt=start_of_this_week
        ).count()

        if new_users_last_week == 0:
            if new_users_this_week == 0:
                percent_change = 0
            else:
                percent_change = 100 
        else:
            percent_change = ((new_users_this_week - new_users_last_week) / new_users_last_week) * 100

        # Envoi au template
        context['new_users_this_week'] = new_users_this_week
        context['new_users_last_week'] = new_users_last_week
        context['percent_change'] = round(percent_change, 2)
        return context

@api_view(['GET'])
@permission_classes([IsStaff])
def user_signups(request):
    data = (
        User.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    return Response(data)


class UserDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'  
    context_object_name = 'user'

class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = User
    form_class = UserUpdateForm  
    template_name = 'user/user_create.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, f' {form.instance.email} has been saved!')
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_update.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


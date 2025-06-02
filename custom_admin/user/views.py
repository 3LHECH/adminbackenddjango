from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
from .forms import ProfileUpdateForm,UserUpdateForm ,UserCreateForm
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.utils.timezone import now, timedelta
from quizz.models import Question,Answer
from django.db.models import Count, Q
from .permissions import StaffRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()

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
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('profile')  
        else:
            messages.error(request, 'Invalid credentials or not a staff account.')
            return redirect('login_user')  
    form_login = CustomUserLogin()
    return render(request, "user/login.html", {"form_login": form_login})



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

@staff_member_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            for field in form.fields:
                if field in form.cleaned_data and field in request.POST:
                    value = form.cleaned_data[field]
                    setattr(user, field, value)
                elif field in request.FILES:
                    value = form.cleaned_data[field]
                    setattr(user, field, value)

            user.save()

            if request.htmx:
                profile_html = render_to_string('user/partials/profile_summary.html', {'user': user})
                form_html = render_to_string('user/partials/profile_form.html', {'form': form})
                return HttpResponse(profile_html + form_html)

            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    if request.htmx:
        form_html = render_to_string('user/partials/profile_form.html', {'form': form})
        return HttpResponse(form_html)

    return render(request, 'user/profile.html', {'form': form})




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
            percent_change = 100 if new_users_this_week else 0
        else:
            percent_change = ((new_users_this_week - new_users_last_week) / new_users_last_week) * 100

        context.update({
            'new_users_this_week': new_users_this_week,
            'new_users_last_week': new_users_last_week,
            'percent_change': round(percent_change, 2)
        })
        return context

@api_view(['GET'])
@staff_member_required
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
    form_class = UserCreateForm
    template_name = 'user/user_create.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, f'{form.instance.email} has been saved!')
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




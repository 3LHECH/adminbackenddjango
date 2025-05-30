from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

# Create your views here.


def custom_admin_dashboard(request):
    if (request.user.is_authenticated) :
        print(request.user)
        return render(request, 'dashboard/home.html')
    else:
        return redirect('profile')  

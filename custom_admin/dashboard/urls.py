from . import views
from django.urls import path

urlpatterns = [  
    path('', views.custom_admin_dashboard, name="home"),
]
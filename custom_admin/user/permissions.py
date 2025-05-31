from rest_framework.permissions import BasePermission
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    


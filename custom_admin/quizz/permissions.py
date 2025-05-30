from rest_framework.permissions import BasePermission
from django.contrib.auth.mixins import UserPassesTestMixin

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
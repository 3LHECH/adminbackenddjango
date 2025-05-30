from django.contrib import admin
from .models import Question,Quizz,Answer
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quizz)

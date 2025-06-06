# forms.py
from django import forms
from .models import Quizz, Question, Answer

class QuizzForm(forms.ModelForm):
    class Meta:
        model = Quizz
        fields = ['title','creator']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quizz', 'type', 'text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['selected_by', 'question', 'text', 'is_correct']
        widgets = {
            'selected_by': forms.CheckboxSelectMultiple()
        }

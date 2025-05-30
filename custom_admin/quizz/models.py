from django.db import models

from django.conf import settings
# Create your models here.

class Quizz(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes',
        null=False
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    class QuestionType(models.TextChoices):
        DATASCIENCE = 'DS', 'Data Science'
        IOT = 'IOT', 'Internet of Things'
        CLOUD = 'CL', 'Cloud Computing'
        GENIE_LOGICIEL = 'Gl', 'Genie Logiciel'

    quizz = models.ForeignKey(
        'Quizz',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    type = models.CharField(
        max_length=3,
        choices=QuestionType.choices
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responses',
        blank=True,
        null=True
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='responses'
    )
    is_correct = models.BooleanField()
    text = models.TextField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.question} - {'Correct' if self.is_correct else 'Wrong'}"
    


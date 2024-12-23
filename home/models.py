from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    due_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Exam(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    exam_date = models.DateField()
    due_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  

    def __str__(self):
        return self.title
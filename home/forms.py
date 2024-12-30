from django import forms
from .models import Assignment, Exam

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'due_date', 'due_time')

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('title', 'description', 'exam_date', 'due_time')

'''class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']'''
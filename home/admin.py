from django.contrib import admin
from .models import Feedback
# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_text', 'created_at')
    search_fields = ('feedback_text', 'user__username')
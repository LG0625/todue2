from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Assignments

    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/new/', views.create_assignment, name='create_assignment'),
    path('assignments/<pk>/edit/', views.edit_assignment, name='edit_assignment'),
    path('assignments/<pk>/delete/', views.delete_assignment, name='delete_assignment'),

    # Exams
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/new/', views.create_exam, name='create_exam'),
    path('exams/<pk>/edit/', views.edit_exam, name='edit_exam'),
    path('exams/<pk>/delete/', views.delete_exam, name='delete_exam'),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("calendar/", views.calendar, name="calendar"),
    path("settings/", views.settings, name="settings"),
    path('add-to-google-calendar/<str:event_type>/<int:event_id>/', views.add_to_google_calendar, name='add_to_google_calendar'),
]
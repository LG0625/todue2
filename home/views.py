from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Assignment
from .forms import AssignmentForm
from .models import Exam
from .forms import ExamForm
from django.conf import settings
from urllib.parse import urlencode

def home(request):
    return render(request, "home/dashboard.html")


def assignment_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    assignments = Assignment.objects.filter(user=request.user)
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        status = request.POST.get('status')
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.status = status
        assignment.save()
    return render(request, 'home/assignment_list.html', {'assignments': assignments})

def create_assignment(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.due_time = request.POST['due_time']
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'home/create_assignment.html', {'form': form})

def edit_assignment(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    assignment = Assignment.objects.get(pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment.due_time = request.POST['due_time']
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'home/edit_assignment.html', {'form': form, 'assignment': assignment})

def delete_assignment(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    Assignment.objects.filter(pk=pk).delete()
    return redirect('assignment_list')

def exam_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    exams = Exam.objects.filter(user=request.user)
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        status = request.POST.get('status')
        exam = Exam.objects.get(id=exam_id)
        exam.status = status
        exam.save()
    return render(request, 'home/exam_list.html', {'exams': exams})

def create_exam(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.due_time = request.POST['due_time']
            exam.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'home/create_exam.html', {'form': form})

def edit_exam(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    exam = Exam.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            exam.due_time = request.POST['due_time']
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'home/edit_exam.html', {'form': form, 'exam': exam})

def delete_exam(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    Exam.objects.filter(pk=pk).delete()
    return redirect('exam_list')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home/dashboard.html")

def calendar(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home/calendar.html")

def settings(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home/settings.html")

def add_to_google_calendar(request, event_type, event_id):
    if event_type == 'assignment':
        event = Assignment.objects.get(id=event_id)
    elif event_type == 'exam':
        event = Exam.objects.get(id=event_id)
    else:
        return render(request, 'error.html', {'error': 'Invalid event type'})
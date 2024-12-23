from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, Exam
from .forms import AssignmentForm, ExamForm
from django.conf import settings
from urllib.parse import urlencode
from django.db.models import Q



def home(request):
    return render(request, "home/dashboard.html")


def assignment_list(request):
    if request.user.is_authenticated:
        assignments = Assignment.objects.filter(user=request.user)
    else:
        assignments = Assignment.objects.filter(user__isnull=True)

    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        status = request.POST.get('status')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        assignment.status = status
        assignment.save()

    return render(request, 'home/assignment_list.html', {'assignments': assignments})


def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            if request.user.is_authenticated:
                assignment.user = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'home/create_assignment.html', {'form': form})


def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.user and assignment.user != request.user:
        return redirect('assignment_list')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'home/edit_assignment.html', {'form': form, 'assignment': assignment})


def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.user is None or (request.user.is_authenticated and assignment.user == request.user):
        assignment.delete()
    return redirect('assignment_list')


def exam_list(request):
    if request.user.is_authenticated:
        exams = Exam.objects.filter(user=request.user)
    else:
        exams = Exam.objects.filter(user__isnull=True)

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        status = request.POST.get('status')
        exam = get_object_or_404(Exam, id=exam_id)
        exam.status = status
        exam.save()

    return render(request, 'home/exam_list.html', {'exams': exams})


def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            if request.user.is_authenticated:
                exam.user = request.user
            exam.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'home/create_exam.html', {'form': form})


def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if exam.user and exam.user != request.user:
        return redirect('exam_list')

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'home/edit_exam.html', {'form': form, 'exam': exam})


def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if exam.user is None or (request.user.is_authenticated and exam.user == request.user):
        exam.delete()
    return redirect('exam_list')


def dashboard(request):
    assignment_count = 0
    exam_count = 0

    if request.user.is_authenticated:
        assignment_count = Assignment.objects.filter(user=request.user).count()
        exam_count = Exam.objects.filter(user=request.user).count()

    return render(request, "home/dashboard.html", {
        'assignment_count': assignment_count,
        'exam_count': exam_count
    })



def calendar(request):
    return render(request, "home/calendar.html")


def settings(request):
    return render(request, "home/settings.html")


def add_to_google_calendar(request, event_type, event_id):
    if event_type == 'assignment':
        event = get_object_or_404(Assignment, id=event_id)
    elif event_type == 'exam':
        event = get_object_or_404(Exam, id=event_id)
    else:
        return render(request, 'error.html', {'error': 'Invalid event type'})

    # Construct Google Calendar Event URL
    params = {
        'action': 'TEMPLATE',
        'text': event.title,
        'dates': f"{event.due_date.isoformat()}T{event.due_time.isoformat()}Z/{event.due_date.isoformat()}T{event.due_time.isoformat()}Z",
        'details': event.description,
        'location': event.location if hasattr(event, 'location') else '',
        'sf': 'true',
        'output': 'xml'
    }
    google_calendar_url = f"https://www.google.com/calendar/render?{urlencode(params)}"
    return redirect(google_calendar_url)

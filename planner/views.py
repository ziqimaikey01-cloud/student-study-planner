from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Assignment
from .forms import CourseForm, AssignmentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request):
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'planner/register.html', {'form': form})

@login_required
def dashboard(request):
    now = timezone.now()
    assignments = Assignment.objects.filter(
        course__owner=request.user,
        completed=False,
        due_date__gte=now
    ).order_by('due_date')[:5]

    total_courses = Course.objects.filter(owner=request.user).count()
    total_assignments = Assignment.objects.filter(course__owner=request.user).count()
    pending_assignments = Assignment.objects.filter(course__owner=request.user, completed=False,due_date__gte=now).count()
    completed_assignments = Assignment.objects.filter(course__owner=request.user, completed=True).count()

    overdue_assignments = Assignment.objects.filter(
        course__owner=request.user,
        completed=False,
        due_date__lt=now
    ).count()

    overdue_list = Assignment.objects.filter(
        course__owner=request.user,
        completed=False,
        due_date__lt=now
    ).order_by('due_date')

    context = {
        'assignments': assignments,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments,
        'overdue_assignments': overdue_assignments,
        'overdue_list': overdue_list,
    }

    return render(request, 'planner/dashboard.html', context)

@login_required
def course_list(request):
    # courses = Course.objects.all()
    courses = Course.objects.filter(owner=request.user)
    return render(request, 'planner/course_list.html', {'courses': courses})

@login_required
def assignment_list(request):
    assignments = Assignment.objects.filter(course__owner=request.user).order_by('due_date')

    for assignment in assignments:
        assignment.overdue = (
            not assignment.completed and assignment.due_date < timezone.now()
        )
    return render(request, 'planner/assignment_list.html', {'assignments': assignments})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            messages.success(request, "Course added successfully.")
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'planner/course_form.html', {'form': form})

@login_required
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST,user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment added successfully.")
            return redirect('assignment_list')
    else:
        form = AssignmentForm(user=request.user)

    return render(request, 'planner/assignment_form.html', {'form': form})

@login_required
def assignment_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id,course__owner=request.user)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment,user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully.")
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment,user=request.user)

    return render(request, 'planner/assignment_form.html', {'form': form})

@login_required
def toggle_assignment(request, assignment_id):
    if request.method != 'POST':
        return redirect('assignment_list')
    assignment = get_object_or_404(Assignment, id=assignment_id,course__owner=request.user)
    assignment.completed = not assignment.completed
    assignment.save()
    messages.success(request, "Assignment status updated successfully.")
    return redirect('assignment_list')

@login_required
def assignment_delete(request, assignment_id):
    if request.method != 'POST':
        return redirect('assignment_list')
    assignment = get_object_or_404(Assignment, id=assignment_id,course__owner=request.user)
    assignment.delete()
    messages.success(request, "Assignment deleted successfully.")
    return redirect('assignment_list')

@login_required
def course_delete(request, course_id):
    if request.method != 'POST':
        return redirect('course_list')

    course = get_object_or_404(Course, id=course_id, owner=request.user)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('course_list')

@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            updated_course = form.save(commit=False)
            updated_course.owner = request.user
            updated_course.save()
            messages.success(request, "Course updated successfully.")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'planner/course_form.html', {'form': form})
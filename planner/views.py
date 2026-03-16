from django.shortcuts import render, redirect
from .models import Course, Assignment
from .forms import CourseForm, AssignmentForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def dashboard(request):
    assignments = Assignment.objects.filter(
        completed=False,
        due_date__gte=timezone.now()
        ).order_by('due_date')[:5]

    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    pending_assignments = Assignment.objects.filter(completed=False).count()
    completed_assignments = Assignment.objects.filter(completed=True).count()

    overdue_assignments = Assignment.objects.filter(
        completed=False,
        due_date__lt=timezone.now()
    ).count()

    overdue_list = Assignment.objects.filter(
        completed=False,
        due_date__lt=timezone.now()
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
    courses = Course.objects.all()
    return render(request, 'planner/course_list.html', {'courses': courses})

@login_required
def assignment_list(request):
    assignments = Assignment.objects.order_by('due_date')

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
            form.save()
            messages.success(request, "Course added successfully.")
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'planner/course_form.html', {'form': form})

@login_required
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment added successfully.")
            return redirect('assignment_list')
    else:
        form = AssignmentForm()

    return render(request, 'planner/assignment_form.html', {'form': form})

@login_required
def assignment_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully.")
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'planner/assignment_form.html', {'form': form})

@login_required
def toggle_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.completed = not assignment.completed
    assignment.save()
    messages.success(request, "Assignment status updated successfully.")
    return redirect('assignment_list')

@login_required
def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    messages.success(request, "Assignment deleted successfully.")
    return redirect('assignment_list')
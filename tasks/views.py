from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('task_list')  # Redirect to task list after registration
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

# Task List View (with filtering by status and due date)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # Show only tasks of the logged-in user

    # Filtering tasks by status and due date
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    due_date = request.GET.get('due_date')
    if due_date:
        tasks = tasks.filter(due_date=due_date)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Create a New Task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associate task with the logged-in user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

# Edit an Existing Task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure only the owner can edit their tasks
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})

# Delete a Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure only the owner can delete their tasks
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})

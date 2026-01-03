from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Todo
from .forms import TodoForm


def home(request):
    """Display all TODOs."""
    todos = Todo.objects.all()
    context = {
        'todos': todos,
        'now': timezone.now(),
    }
    return render(request, 'todos/home.html', context)


def create_todo(request):
    """Create a new TODO."""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'TODO created successfully!')
            return redirect('todos:home')
    else:
        form = TodoForm()
    
    return render(request, 'todos/todo_form.html', {
        'form': form,
        'title': 'Create TODO'
    })


def edit_todo(request, pk):
    """Edit an existing TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'TODO updated successfully!')
            return redirect('todos:home')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todos/todo_form.html', {
        'form': form,
        'todo': todo,
        'title': 'Edit TODO'
    })


def delete_todo(request, pk):
    """Delete a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'TODO deleted successfully!')
        return redirect('todos:home')
    
    return render(request, 'todos/todo_confirm_delete.html', {
        'todo': todo
    })


def toggle_resolve(request, pk):
    """Toggle the resolved status of a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()
    
    status = 'resolved' if todo.is_resolved else 'unresolved'
    messages.success(request, f'TODO marked as {status}!')
    return redirect('todos:home')


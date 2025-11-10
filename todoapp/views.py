from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('todo-page')
    return render(request, 'todoapp/home.html', {})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('todo-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('todo-page')
        else:
            messages.error(request, message="Wrong credentials")
            return redirect('login-page')

    return render(request, 'todoapp/login.html', {})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home-page')


def register(request):
    if request.user.is_authenticated:
        return redirect('todo-page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        get_all_users_by_username = User.objects.filter(username = username)
        if get_all_users_by_username:
            messages.error(request, message="Username already exists.")
            return redirect('registration-page')
        
        if len(password) < 4:
            messages.error(request, message="Password must be atleast 4 characters.")
            return redirect('registration-page')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, message=f"New user {username} created")
        return redirect('login-page')
        
    return render(request, 'todoapp/register.html', {})


@login_required
def todopage(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_task = Todo(user=request.user, task_title=task)
        new_task.save()
        return redirect('todo-page')
    
    all_tasks = Todo.objects.filter(user=request.user)
    current_user = request.user.username

    context = {
        'tasks': all_tasks,
        'username': current_user
    }
    return render(request, 'todoapp/todo.html', context)

# with delete conformation
# def delete_task(request, task_id):
#     task = get_object_or_404(Todo, id=task_id, user=request.user)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('todo-page')
#     return render(request, 'todoapp/delete_confirm.html', {'task': task})


# derect delete (no confirmation)
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('todo-page')


# -- with confitmation
# def update_task(request, task_id):
#     task = get_object_or_404(Todo, id=task_id, user=request.user)
#     if request.method == 'POST':
#         new_title = request.POST.get('task')
#         task.task_title = new_title
#         task.save()
#         return redirect('todo-page')
#     return render(request, 'todoapp/update.html', {'task': task})

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Todo, id=task_id, user=request.user)
    if request.method == 'POST':
        task.status = True
        task.save()
    return redirect('todo-page')
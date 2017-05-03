from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from appTodolist.models import Task
from django.views.decorators.csrf import csrf_exempt


def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.order_by('done', "-priority")
        return render(request, 'appTodoList/tasks.html', {
            'tasks': tasks
        })
    else:
        return HttpResponseNotAllowed(['GET'])


def add_task(request):
    if request.method == 'POST':
        if request.POST.get('name'):
            task = Task(name=request.POST.get('name'))
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def change_state_task(request):
    if request.method == 'POST':
        task_id = request.POST.get("id")
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.change_state()
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get("id")
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def edit_name(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        task_name = request.POST.get('name')
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.name = task_name
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def increase_priority(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.increase_priority()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def decrease_priority(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.decrease_priority()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])
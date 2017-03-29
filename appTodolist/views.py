from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from appTodolist.models import Task


def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
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


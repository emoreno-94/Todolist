from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from appTodolist.models import Task


def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        return render(request, 'appTodoList/tasks.html', {
            'tasks': tasks
        })
    else:
        return HttpResponseNotAllowed(['GET'])

from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from appTodolist.models import Task
from django.views.decorators.csrf import csrf_exempt


def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        return render(request, 'appTodoList/tasks.html', {
            'tasks': tasks
        })
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        if request.POST.get('name'):
            task = Task(name=request.POST.get('name'))
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def set_done_task(request):
    if request.method == 'POST':
        task_id = request.POST.get("id")
        if task_id is not None:
            task = Task.objects.get(pk=int(task_id))
            task.complete()
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])
from django.http import HttpResponseNotAllowed, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
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


@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get("id")
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
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
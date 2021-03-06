from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from appTodolist.models import Task, TaskList


def get_tasks(request):
    if request.method == 'GET':
        lists = TaskList.objects.order_by("-priority")
        return render(request, 'appTodoList/new_tasks.html', {
            'task_lists': lists
        })
    else:
        return HttpResponseNotAllowed(['GET'])


def add_task(request):
    if request.method == 'POST':
        name = request.POST.get('task_name')
        id = request.POST.get('list_id')
        if name and id:
            task_list = TaskList.objects.get(pk=id)
            Task.objects.create(name=name, task_list=task_list)
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def add_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            TaskList.objects.create(name=name)
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


def increase_priority_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.increase_priority()
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def decrease_priority_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        if task_id is not None:
            task = get_object_or_404(Task, id=task_id)
            task.decrease_priority()
            task.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def increase_priority_list(request):
    if request.method == 'POST':
        list_id = request.POST.get('id')
        if list_id is not None:
            list1 = get_object_or_404(TaskList, id=list_id)
            list1.increase_priority()
            list1.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def decrease_priority_list(request):
    if request.method == 'POST':
        list_id = request.POST.get('id')
        if list_id is not None:
            list1 = get_object_or_404(TaskList, id=list_id)
            list1.decrease_priority()
            list1.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])


def delete_list(request):
    if request.method == 'POST':
        list_id = request.POST.get("id")
        if list_id is not None:
            list1 = get_object_or_404(TaskList, id=list_id)
            list1.delete()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])

def edit_list(request):
    if request.method == 'POST':
        list_id = request.POST.get("id")
        task_list_name = request.POST.get('name')
        if list_id is not None:
            list1 = get_object_or_404(TaskList, id=list_id)
            list1.name = task_list_name
            list1.save()
        return redirect('tasks:get_tasks')
    else:
        return HttpResponseNotAllowed(['POST'])
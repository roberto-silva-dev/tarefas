from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    form = TaskForm()
    return render(request, 'index.html', {'tasks': tasks, 'form': form})

@csrf_exempt
def task_create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = TaskForm(data)
        if form.is_valid():
            task = form.save()
            return JsonResponse({'id': task.id, 'title': task.title, 'completed': task.completed}, status=201)
    return JsonResponse({'error': 'Invalid data'}, status=400)


@csrf_exempt
def task_handle(request, task_id):
    if request.method == 'PATCH':
        return task_complete(request, task_id)
    elif request.method == 'DELETE':
        return task_delete(request, task_id)
    
def task_complete(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if request.method == "PATCH":
            task.completed = not task.completed
            task.save()
            return JsonResponse({'id': task.id, 'completed': task.completed})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

def task_delete(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if request.method == "DELETE":
            task.delete()
            return JsonResponse({'message': 'Task deleted'}, status=204)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

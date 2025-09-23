from .forms import TaskForm
from .models import Task
from .services.ai_parser import call_gemini_api
from django.shortcuts import render, redirect

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)

            # 呼叫 Gemini API
            ai_result = call_gemini_api(task.title, task.description)
            task.estimated_time = ai_result['estimated_time']
            task.environment = ai_result['environment']
            task.priority = ai_result['priority']

            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

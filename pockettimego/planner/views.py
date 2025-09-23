from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from .utils import find_free_slots, recommend_today
from datetime import datetime

def upload_schedule(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('today_schedule')
    else:
        form = CourseForm()
    return render(request, 'tasks/upload_schedule.html', {'form': form})

def today_schedule(request):
    weekday = datetime.today().isoweekday()
    courses = request.user.courses.filter(weekday=weekday).order_by('start_time')
    free_slots = find_free_slots(request.user, weekday)
    return render(request, 'tasks/today_schedule.html', {'courses': courses, 'free_slots': free_slots})

def find_free_slots_view(request):
    weekday = datetime.today().isoweekday()
    free_slots = find_free_slots(request.user, weekday)
    return render(request, 'tasks/free_slots.html', {'free_slots': free_slots})

def recommend_today_view(request):
    weekday = datetime.today().isoweekday()
    # 這裡示範固定任務，也可從資料庫拉
    tasks = [
        {"title": "寫報告", "estimated_time": 45, "preferred_location_type": "quiet"},
        {"title": "複習程式", "estimated_time": 30, "preferred_location_type": "charging"}
    ]
    recommendations = recommend_today(request.user, weekday, tasks)
    return render(request, 'tasks/recommend_today.html', {'recommendations': recommendations})

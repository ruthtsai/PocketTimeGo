from datetime import datetime, time, timedelta
from .models import Course, Location
# utils.py
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    計算兩個座標的球面距離（單位：公尺）
    """
    R = 6371000  # 地球半徑，公尺
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def get_distance_minutes(location1, location2):
    """
    計算兩個 Location 物件之間的步行時間（每100公尺5分鐘）
    """
    if not (location1 and location2):
        return 0
    if location1 == location2:
        return 0
    if not (location1.latitude and location1.longitude and location2.latitude and location2.longitude):
        return 10  # 座標缺失時預設 10 分鐘

    distance_m = haversine_distance(
        location1.latitude, location1.longitude,
        location2.latitude, location2.longitude
    )
    walking_minutes = distance_m / 100 * 5  # 每100公尺5分鐘
    return int(round(walking_minutes))

def find_free_slots(user, weekday):
    courses = user.courses.filter(weekday=weekday).order_by('start_time')
    free_slots = []

    day_start = time(8,0)
    day_end = time(22,0)
    prev_end = day_start
    prev_location = None

    for course in courses:
        travel = get_distance_minutes(prev_location, course.location)
        adjusted_prev_end = (datetime.combine(datetime.today(), prev_end) + timedelta(minutes=travel)).time()
        if course.start_time > adjusted_prev_end:
            free_slots.append((adjusted_prev_end, course.start_time))
        prev_end = course.end_time
        prev_location = course.location

    if prev_end < day_end:
        free_slots.append((prev_end, day_end))

    return free_slots

def recommend_today(user, weekday, tasks):
    """
    tasks: list of dicts, e.g.
    [{'title': '寫報告', 'estimated_time': 45, 'preferred_location_type': 'quiet'}]
    """
    free_slots = find_free_slots(user, weekday)
    recommendations = []

    for task in tasks:
        task_time = task['estimated_time']
        loc_type = task.get('preferred_location_type', 'general')
        loc_candidates = Location.objects.filter(type=loc_type)
        
        for slot_start, slot_end in free_slots:
            slot_duration = (datetime.combine(datetime.today(), slot_end) - datetime.combine(datetime.today(), slot_start)).total_seconds() / 60
            if slot_duration >= task_time:
                recommendations.append({
                    "task": task['title'],
                    "start_time": slot_start,
                    "end_time": (datetime.combine(datetime.today(), slot_start) + timedelta(minutes=task_time)).time(),
                    "location": loc_candidates.first().name if loc_candidates.exists() else "任意地點"
                })
                break
    return recommendations

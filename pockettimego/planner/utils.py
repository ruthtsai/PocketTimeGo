from datetime import datetime, time, timedelta
from .models import Course, Location
from task.models import Task

# utils.py
import math

# Task.environment 與 Location.type 對應表
ENV_TO_LOCATION = {
    "laptop": ["library", "computer_lab", "cafe", "charging"],
    "writing": ["library", "cafe", "dorm"],
    "tablet": ["library", "computer_lab", "cafe", "charging"],
    "quiet": ["library", "dorm", "charging"],
    "group": ["cafe", "outdoor"],
    "exercise": ["gym", "outdoor"],
    "eat": ["cafe", "dorm"],
    "laundry": ["dorm"],
    "relax": ["dorm", "outdoor", "cafe"],
    "other": ["general"]
}

def match_task_to_location(task: Task):
    """
    根據 task.environment 推薦可能的地點清單
    """
    env = task.environment
    possible_types = ENV_TO_LOCATION.get(env, ["general"])
    return Location.objects.filter(type__in=possible_types)

def get_distance_minutes(location1, location2):
    """
    計算兩個 Location 物件之間的步行時間
    使用經緯度換算平面距離，再用 Δx + Δy (曼哈頓距離)
    每 100 公尺 = 5 分鐘
    """
    if not (location1 and location2):
        return 0
    if location1 == location2:
        return 0
    if location1.latitude is None or location1.longitude is None \
       or location2.latitude is None or location2.longitude is None:
        return 10  # 缺少座標時預設 10 分鐘

    # 取平均緯度，估算經度換算比例
    avg_lat = math.radians((location1.latitude + location2.latitude) / 2.0)
    meters_per_lat = 111_000  # 1 緯度 ≈ 111 km
    meters_per_lon = 111_000 * math.cos(avg_lat)  # 經度要乘 cos(緯度)

    dx = abs(location1.longitude - location2.longitude) * meters_per_lon
    dy = abs(location1.latitude - location2.latitude) * meters_per_lat

    distance_m = dx + dy  # 曼哈頓距離
    walking_minutes = distance_m / 100 * 5  # 每 100m 5 分鐘
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
    Prototype: 最簡可執行的最佳化推薦 (優化版)
    - 按 priority 排序
    - 找出能放進 free_slot 的任務
    - 使用 match_task_to_location() 篩選地點
    - 選擇距離最近的地點
    """

    free_slots = find_free_slots(user, weekday)
    recommendations = []

    # 按 priority 排序 (1=最高, 預設=3)
    tasks = sorted(tasks, key=lambda x: x.get("priority", 3))
    prev_location = None

    for task in tasks:
        task_time = task.get("estimated_time", 30)  # 預設30分鐘
        env = task.get("environment", "general")

        # ✅ 改用 utils.match_task_to_location()
        loc_candidates = match_task_to_location(task)
        if not loc_candidates.exists():
            loc_candidates = Location.objects.all()

        # 遍歷 free slots
        for slot_start, slot_end in free_slots:
            slot_duration = (
                datetime.combine(datetime.today(), slot_end)
                - datetime.combine(datetime.today(), slot_start)
            ).total_seconds() / 60

            best_choice = None
            best_score = float("inf")

            for loc in loc_candidates:
                travel = get_distance_minutes(prev_location, loc) if prev_location else 0
                available_time = slot_duration - travel

                if available_time >= task_time:
                    # 簡單最佳化策略 = travel + |slot_duration - task_time|
                    score = travel + abs(slot_duration - task_time)

                    if score < best_score:
                        best_score = score
                        best_choice = {
                            "task": task["title"],
                            "start_time": slot_start,
                            "end_time": (
                                datetime.combine(datetime.today(), slot_start)
                                + timedelta(minutes=task_time)
                            ).time(),
                            "location": loc.name,
                            "travel_minutes": travel,
                        }

            if best_choice:
                recommendations.append(best_choice)
                prev_location = loc  # 下一個任務的起點
                break  # 任務已安排 → 換下一個任務

    return recommendations

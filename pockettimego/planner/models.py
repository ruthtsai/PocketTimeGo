from django.db import models
from django.contrib.auth import get_user_model

class Location(models.Model):
    LOCATION_TYPES = [
        ("quiet", "安靜空間"),
        ("charging", "可充電"),
        ("general", "一般空間"),
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    latitude = models.FloatField(null=True, blank=True)   # 緯度
    longitude = models.FloatField(null=True, blank=True)  # 經度

    def __str__(self):
        return self.name

class Course(models.Model):
    WEEKDAYS = [
        (1, "星期一"),
        (2, "星期二"),
        (3, "星期三"),
        (4, "星期四"),
        (5, "星期五"),
        (6, "星期六"),
        (7, "星期日"),
    ]
   
    name = models.CharField(max_length=100)
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_weekday_display()})"
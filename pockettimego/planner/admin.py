# admin.py
from django.contrib import admin
from .models import Course, Location

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'weekday', 'start_time', 'end_time', 'location')
    list_filter = ('weekday', 'location')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude')
    list_filter = ('type',)
    search_fields = ('name',)

from django.db import models

class Task(models.Model):
    ENV_CHOICES = [
        ('電腦', '電腦'),
        ('紙筆', '紙筆'),
        ('平板', '平板'),
        ('安靜空間', '安靜空間'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)  # AI 預估
    environment = models.CharField(max_length=20, choices=ENV_CHOICES, blank=True)
    priority = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

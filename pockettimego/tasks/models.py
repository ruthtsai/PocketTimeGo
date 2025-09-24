from django.db import models

class Task(models.Model):
    ENV_CHOICES = [
        ("laptop", "需要電腦"),
        ("writing", "需要紙筆"),
        ("tablet", "需要平板"),
        ("quiet", "安靜環境"),
        ("group", "團隊合作"),
        ("exercise", "運動空間"),
        ("eat", "飲食/邊吃邊做"),
        ("laundry", "洗衣相關"),
        ("relax", "休閒/放鬆"),
        ("other", "其他"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    estimated_time = models.IntegerField(null=True, blank=True)  # AI 預估
    priority = models.IntegerField(default=3)
    environment = models.CharField(max_length=20, choices=ENV_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

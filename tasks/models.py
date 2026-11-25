from django.conf import settings
from django.db import models


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        NORMAL = "normal", "Обычный"
        HIGH = "high", "Высокий"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.NORMAL)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["completed", "-priority", "due_date"]


    def __str__(self):
        return self.title

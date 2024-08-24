from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('completed', 'Completed')])
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    Isdelete=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

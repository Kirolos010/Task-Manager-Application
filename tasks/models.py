from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()  
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

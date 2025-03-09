from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):

    title = models.CharField(max_length=200)

    TODO_CATEGORIES = (
        ("Business","Business"),
        ("Personal","Personal")
    )

    category = models.CharField(max_length=200, choices=TODO_CATEGORIES, default="Personal")

    created_at = models.DateTimeField(auto_now_add=True)

    due_date = models.DateField(blank=True, null=True)

    PRIORITY_CHOICES = (
        ("Low","Low"),
        ("Medium","Medium"),
        ("High","High")
    )

    priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES, default="Low")

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In_Progress','In Progress'),
        ('Completed', 'Completed')
    )

    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Pending")

    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
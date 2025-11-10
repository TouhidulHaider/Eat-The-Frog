from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.task_title

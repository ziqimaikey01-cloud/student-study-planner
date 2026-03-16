from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)


class Position(models.Model):
    name = models.CharField(max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    project = models.ManyToManyField(Project)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Urgent", "Immediate attention required"),
        ("High", "Important, needs action soon"),
        ("Medium", "Can wait"),
        ("Low", "Low importance"),
        ("Optional", "Can be done if time permits"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, default="Urgent")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

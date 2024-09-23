from django.db.models.signals import post_migrate
from django.dispatch import receiver
from catalog.models import TaskType


@receiver(post_migrate)
def create_default_task_types(sender, **kwargs):
    default_task_types = ["Bug", "New feature", "Breaking change", "Refactoring", "QA"]

    for task_type in default_task_types:
        TaskType.objects.get_or_create(name=task_type)


@receiver(post_migrate)
def create_default_positions(sender, **kwargs):
    default_position_list = ["Developer", "Project Manager", "QA", "Designer", "DevOps"]

    for position in default_position_list:
        TaskType.objects.get_or_create(name=position)

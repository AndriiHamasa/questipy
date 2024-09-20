from django.db.models.signals import post_migrate
from django.dispatch import receiver
from catalog.models import TaskType


@receiver(post_migrate)
def create_default_task_types(sender, **kwargs):
    default_task_types = [
        'bug', 'new feature', 'breaking change', 'refactoring', 'QA'
    ]

    for task_type in default_task_types:
        TaskType.objects.get_or_create(name=task_type)

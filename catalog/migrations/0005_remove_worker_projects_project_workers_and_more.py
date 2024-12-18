# Generated by Django 5.1.1 on 2024-09-20 05:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_rename_project_worker_projects"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="worker",
            name="projects",
        ),
        migrations.AddField(
            model_name="project",
            name="workers",
            field=models.ManyToManyField(
                related_name="projects", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="assignees",
            field=models.ManyToManyField(
                related_name="assigned_tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="catalog.project",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="task_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="catalog.tasktype",
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="position",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workers",
                to="catalog.position",
            ),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-20 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_alter_task_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["-priority", "deadline"]},
        ),
        migrations.AddField(
            model_name="project",
            name="positions",
            field=models.ManyToManyField(
                related_name="projects", to="catalog.position"
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="task_types",
            field=models.ManyToManyField(
                related_name="projects", to="catalog.tasktype"
            ),
        ),
    ]
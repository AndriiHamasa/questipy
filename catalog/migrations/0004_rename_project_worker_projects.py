# Generated by Django 5.1.1 on 2024-09-20 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_worker_project"),
    ]

    operations = [
        migrations.RenameField(
            model_name="worker",
            old_name="project",
            new_name="projects",
        ),
    ]
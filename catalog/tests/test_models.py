from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import TaskType, Position, Project, Task


class ModelsTestCase(TestCase):

    def test_task_type_fields(self):
        task_type = TaskType.objects.create(name="Development")
        self.assertEqual(task_type._meta.get_field('name').max_length, 255)

    def test_task_type_str_method(self):
        task_type = TaskType.objects.create(name="Development")
        return self.assertEqual(str(task_type),task_type.name)

    def test_position_fields(self):
        position = Position.objects.create(name="Manager")
        self.assertEqual(position._meta.get_field('name').max_length, 255)

    def test_position_str_method(self):
        position = TaskType.objects.create(name="developer")
        return self.assertEqual(str(position), position.name)

    def test_project_fields(self):
        project = Project.objects.create(name="New Project", description="Project Description")
        self.assertEqual(project._meta.get_field('name').max_length, 255)
        self.assertEqual(project._meta.get_field('description').null, False)
        self.assertTrue(project._meta.get_field('workers').many_to_many)

    def test_project_str_method(self):
        project = Project.objects.create(name="test", description="test")
        return self.assertEqual(str(project), project.name)

    def test_get_user_model_worker(self):
        worker = get_user_model().objects.create_user(
            email="get_user_model()@test.com", password="password123"
        )
        self.assertEqual(worker._meta.get_field('email').max_length, 50)
        self.assertTrue(worker._meta.get_field('email').unique)

    def test_worker_str_method(self):
        worker = get_user_model().objects.create(username="test", password="test1234", first_name="test", last_name="test")
        return self.assertEqual(str(worker), f"{worker.first_name} {worker.last_name}")

    def test_task_fields(self):
        task = Task.objects.create(
            name="Task",
            description="Task Description",
            deadline="2024-12-31 12:00:00",
            priority="High",
            task_type=TaskType.objects.create(name="Development"),
            project=Project.objects.create(name="Test Project", description="Test")
        )
        self.assertEqual(task._meta.get_field('name').max_length, 255)
        self.assertEqual(list(task._meta.get_field('priority').choices), list(Task.PRIORITY_CHOICES))
        self.assertEqual(task._meta.get_field('is_completed').default, False)
        self.assertTrue(task._meta.get_field('assignees').many_to_many)
        self.assertTrue(task._meta.get_field('project').is_relation)

    def test_task_ordering(self):
        self.assertEqual(Task._meta.ordering, ['-priority', 'deadline'])

    def test_task_str_method(self):
        task = Task.objects.create(
            name="Task",
            description="Task Description",
            deadline="2024-12-31 12:00:00",
            priority="High",
            task_type=TaskType.objects.create(name="Development"),
            project=Project.objects.create(name="Test Project", description="Test")
        )
        return self.assertEqual(str(task), f"{task.name} ({task.priority})")

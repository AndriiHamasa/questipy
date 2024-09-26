from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Project, Worker, TaskType, Task, Position


WORKER_LIST_URL = reverse("catalog:worker-list")
WORKER_CREATE_URL = reverse("catalog:worker-create")

TASK_LIST_URL = reverse("catalog:project-task-list", args=[1])
TASK_CREATE_URL = reverse("catalog:project-task-create", args=[1])

POSITION_LIST_URL = reverse("catalog:position-list")
POSITION_CREATE_URL = reverse("catalog:position-create")

TASK_TYPE_LIST_URL = reverse("catalog:task-type-list")
TASK_TYPE_CREATE_URL = reverse("catalog:task-type-create")


class PublicProjectTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("catalog:project-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateProjectTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@example.com",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_project_list(self):
        Project.objects.create(name="Project 1")
        Project.objects.create(name="Project 2")
        res = self.client.get(reverse("catalog:project-list"))
        project_list = Project.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["object_list"]), list(project_list))
        self.assertTemplateUsed(res, "catalog/project_list.html")

    def test_delete_project(self):
        project = Project.objects.create(name="Project to delete")

        response = self.client.post(
            reverse("catalog:project-delete", args=[project.pk])
        )
        self.assertEqual(Project.objects.filter(pk=project.pk).count(), 0)
        self.assertRedirects(response, reverse("catalog:project-list"))


class PublicWorkerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_worker_create_login_required(self):
        res = self.client.get(WORKER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@example.com",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_worker_list(self):
        Worker.objects.create(username="worker1", email="worker1@example.com")
        Worker.objects.create(username="worker2", email="worker2@example.com")
        res = self.client.get(WORKER_LIST_URL)
        worker_list = Worker.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["object_list"]), list(worker_list))
        self.assertTemplateUsed(res, "catalog/worker_list.html")

    def test_delete_worker(self):
        worker = Worker.objects.create(
            username="worker_to_delete", email="worker@example.com"
        )
        response = self.client.post(reverse("catalog:worker-delete", args=[worker.pk]))
        self.assertFalse(Worker.objects.filter(pk=worker.pk).exists())
        self.assertRedirects(response, reverse("catalog:worker-list"))


class PublicTaskTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_create_login_required(self):
        res = self.client.get(TASK_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@example.com",
            password="test1234",
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Task Type")
        self.project = Project.objects.create(
            name="Test Project", description="Project description"
        )

    def test_retrieve_task_list(self):
        Task.objects.create(
            name="Task 1",
            project=self.project,
            deadline="2024-12-31 12:00:00",
            task_type=self.task_type,
        )
        Task.objects.create(
            name="Task 2",
            project=self.project,
            deadline="2024-12-31 13:00:00",
            task_type=self.task_type,
        )
        res = self.client.get(TASK_LIST_URL.replace("1", str(self.project.pk)))
        task_list = Task.objects.filter(project=self.project)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["object_list"]), list(task_list))
        self.assertTemplateUsed(res, "catalog/task_list.html")

    def test_delete_task(self):
        task = Task.objects.create(
            name="Task to delete",
            description="Delete this task",
            project=self.project,
            deadline="2024-12-31 12:00:00",
            task_type=self.task_type,
        )
        response = self.client.post(
            reverse("catalog:project-task-delete", args=[self.project.pk, task.pk])
        )
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        self.assertRedirects(
            response, reverse("catalog:project-task-list", args=[self.project.pk])
        )


class PublicPositionTest(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_position_create_login_required(self):
        res = self.client.get(POSITION_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@example.com",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_position_list(self):
        Position.objects.create(name="Manager")
        Position.objects.create(name="Developer")
        res = self.client.get(POSITION_LIST_URL)
        position_list = Position.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["object_list"]), list(position_list))
        self.assertTemplateUsed(res, "catalog/position_list.html")

    def test_create_position(self):
        form_data = {
            "name": "New Position",
        }

        response = self.client.post(POSITION_CREATE_URL, form_data)
        new_position = Position.objects.get(name=form_data["name"])

        self.assertEqual(new_position.name, form_data["name"])
        self.assertRedirects(response, POSITION_LIST_URL)

    def test_update_position(self):
        position = Position.objects.create(name="Old Position")
        form_data = {
            "name": "Updated Position",
        }

        response = self.client.post(
            reverse("catalog:position-update", args=[position.pk]), form_data
        )
        position.refresh_from_db()

        self.assertEqual(position.name, form_data["name"])
        self.assertRedirects(response, POSITION_LIST_URL)

    def test_delete_position(self):
        position = Position.objects.create(name="Position to delete")
        response = self.client.post(
            reverse("catalog:position-delete", args=[position.pk])
        )
        self.assertFalse(Position.objects.filter(pk=position.pk).exists())
        self.assertRedirects(response, POSITION_LIST_URL)


class PublicTaskTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_TYPE_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_type_create_login_required(self):
        res = self.client.get(TASK_TYPE_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@example.com",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_create_task_type(self):
        form_data = {
            "name": "New TaskType",
        }

        response = self.client.post(TASK_TYPE_CREATE_URL, form_data)
        new_task_type = TaskType.objects.get(name=form_data["name"])

        self.assertEqual(new_task_type.name, form_data["name"])
        self.assertRedirects(response, TASK_TYPE_LIST_URL)

    def test_update_task_type(self):
        task_type = TaskType.objects.create(name="Old TaskType")
        form_data = {
            "name": "Updated TaskType",
        }

        response = self.client.post(
            reverse("catalog:task-type-update", args=[task_type.pk]), form_data
        )
        task_type.refresh_from_db()

        self.assertEqual(task_type.name, form_data["name"])
        self.assertRedirects(response, TASK_TYPE_LIST_URL)

    def test_delete_task_type(self):
        task_type = TaskType.objects.create(name="TaskType to delete")
        response = self.client.post(
            reverse("catalog:task-type-delete", args=[task_type.pk])
        )
        self.assertFalse(TaskType.objects.filter(pk=task_type.pk).exists())
        self.assertRedirects(response, TASK_TYPE_LIST_URL)

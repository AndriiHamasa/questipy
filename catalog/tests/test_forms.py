from django.test import TestCase
from django import forms
from catalog.forms import (
    ProjectForm,
    ProjectAddWorkerForm,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    TaskForm,
    TaskAddWorkersForm,
    ProjectNameSearchForm,
    WorkerUsernameSearchForm,
    TaskNameSearchForm,
    PositionNameSearchForm,
    TaskTypeNameSearchForm,
)


class ProjectFormTest(TestCase):
    def test_project_form_fields(self):
        form = ProjectForm()

        self.assertIsInstance(
            form.fields["workers"].widget, forms.CheckboxSelectMultiple
        )
        self.assertEqual(
            form.fields["workers"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )

        self.assertIsInstance(form.fields["description"].widget, forms.Textarea)
        self.assertEqual(form.fields["description"].widget.attrs["rows"], 4)
        self.assertEqual(
            form.fields["description"].widget.attrs["style"],
            "resize: none; overflow: auto; background-color: #1a252f; color: white;",
        )

        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )


class ProjectAddWorkerFormTest(TestCase):
    def test_project_add_worker_form_fields(self):
        form = ProjectAddWorkerForm()

        self.assertIsInstance(
            form.fields["workers"].widget, forms.CheckboxSelectMultiple
        )
        self.assertEqual(
            form.fields["workers"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )


class WorkerCreationFormTest(TestCase):
    def test_worker_creation_form_styles(self):
        form = WorkerCreationForm()

        for field in form.fields.values():
            self.assertEqual(
                field.widget.attrs["style"], "background-color: #1a252f; color: white;"
            )


class WorkerPositionUpdateFormTest(TestCase):
    def test_worker_position_update_form_fields(self):
        form = WorkerPositionUpdateForm()

        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["username"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )

        self.assertIsInstance(form.fields["position"].widget, forms.Select)
        self.assertEqual(
            form.fields["position"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )


class TaskFormTest(TestCase):
    def test_task_form_fields(self):
        form = TaskForm()

        self.assertIsInstance(
            form.fields["assignees"].widget, forms.CheckboxSelectMultiple
        )
        self.assertEqual(
            form.fields["assignees"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )

        self.assertIsInstance(form.fields["deadline"].widget, forms.DateTimeInput)
        self.assertEqual(
            form.fields["deadline"].widget.attrs["style"],
            "background-color: #1a252f; color: white;",
        )

        self.assertIsInstance(form.fields["description"].widget, forms.Textarea)
        self.assertEqual(
            form.fields["description"].widget.attrs["style"],
            "resize: none; overflow: auto; background-color: #1a252f; color: white;",
        )


class TaskAddWorkersFormTest(TestCase):
    def test_task_add_workers_form_fields(self):
        form = TaskAddWorkersForm()

        self.assertIsInstance(
            form.fields["assignees"].widget, forms.CheckboxSelectMultiple
        )


class SearchFormsTest(TestCase):
    def test_project_name_search_form(self):
        form = ProjectNameSearchForm()
        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )

    def test_worker_username_search_form(self):
        form = WorkerUsernameSearchForm()
        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Search by username"
        )

    def test_task_name_search_form(self):
        form = TaskNameSearchForm()
        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )

    def test_position_name_search_form(self):
        form = PositionNameSearchForm()
        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )

    def test_task_type_name_search_form(self):
        form = TaskTypeNameSearchForm()
        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Project, Task


class ProjectForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"style": "background-color: #1a252f; color: white;"}
        ),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "style": "resize: none; overflow: auto; background-color: #1a252f; color: white;",
            }
        )
    )

    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"style": "background-color: #1a252f; color: white;"}
            ),
        }


class ProjectAddWorkerForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"style": "background-color: #1a252f; color: white;"}
        ),
    )

    class Meta:
        model = Project
        fields = ("workers",)


class WorkerCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""

            field.widget.attrs.update(
                {"style": "background-color: #1a252f; color: white;"}
            )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "position",
        )


class WorkerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "position")

        widgets = {
            "username": forms.TextInput(
                attrs={"style": "background-color: #1a252f; color: white;"}
            ),
            "position": forms.Select(
                attrs={"style": "background-color: #1a252f; color: white;"}
            ),
        }


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_pk = self.initial.get("project_pk")
        print("project_pk exist?:", project_pk)
        if project_pk:
            project = Project.objects.get(pk=project_pk)
            self.fields["assignees"].queryset = project.workers.all()
        else:
            self.fields["assignees"].queryset = get_user_model().objects.all()

    assignees = forms.ModelMultipleChoiceField(
        queryset=Project.objects.none(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"style": "background-color: #1a252f; color: white;"}
        ),
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "style": "background-color: #1a252f; color: white;",
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "style": "resize: none; overflow: auto; background-color: #1a252f; color: white;",
            }
        )
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"style": "background-color: #1a252f; color: white;"}
            ),
            "priority": forms.Select(
                attrs={"style": "background-color: #1a252f; color: white;"}
            ),
            "task_type": forms.Select(
                attrs={"style": "background-color: #1a252f; color: white;"}
            ),
        }


class TaskAddWorkersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_pk = self.initial.get("project_pk")
        print("project_pk exist?:", project_pk)
        if project_pk:
            project = Project.objects.get(pk=project_pk)
            self.fields["assignees"].queryset = project.workers.all()
        else:
            self.fields["assignees"].queryset = get_user_model().objects.all()

    assignees = forms.ModelMultipleChoiceField(
        queryset=Project.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Task
        fields = ("assignees",)


class ProjectNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        label="",
    )


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
        label="",
    )


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        label="",
    )


class PositionNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        label="",
    )


class TaskTypeNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        label="",
    )

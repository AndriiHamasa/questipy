from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Project, Task


class ProjectForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Project
        fields = "__all__"


class WorkerCreationForm(UserCreationForm):
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
        fields = ("position", )


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'style': 'resize: vertical;'
        })
    )
    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees")


class TaskAddWorkersForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    class Meta:
        model = Task
        fields = ("assignees", )

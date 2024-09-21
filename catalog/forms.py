from django import forms
from django.contrib.auth import get_user_model

from catalog.models import Project


class ProjectForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Project
        fields = "__all__"
from django import forms
from django.contrib.auth.forms import authenticate, get_user_model, AuthenticationForm

Worker = get_user_model()


class WorkerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "position",
            "password",
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email_check = Worker.objects.filter(email=email)
        username_check = Worker.objects.filter(username=username)
        if email_check.exists() or username_check.exists():
            raise forms.ValidationError("This Email or username already exists")
        if len(password) < 5:
            raise forms.ValidationError(
                "Your password should have more than 5 characters"
            )
        return super(WorkerRegisterForm, self).clean(*args, **kwargs)


class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=150,
        required=True,
    )
    password = forms.CharField(widget=forms.PasswordInput)

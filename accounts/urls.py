from django.urls import path
from accounts.views import (
    signup_view,
    verify_email,
    verify_email_done,
    verify_email_confirm,
    verify_email_complete,
    WorkerLoginView,
    WorkerLogoutView,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("verify-email/", verify_email, name="verify-email"),
    path("verify-email/done/", verify_email_done, name="verify-email-done"),
    path(
        "verify-email-confirm/<uidb64>/<token>/",
        verify_email_confirm,
        name="verify-email-confirm",
    ),
    path("verify-email/complete/", verify_email_complete, name="verify-email-complete"),
    path("login/", WorkerLoginView.as_view(), name="login"),
    path("logout/", WorkerLogoutView.as_view(), name="logout"),
]

app_name = "accounts"

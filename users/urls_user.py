from django.urls import path
from . import views

app_name = "user"
# user/
urlpatterns = [
    path(
        "confirm-email/<uidb64>/<token>",
        views.ConfirmRegisterView.as_view(),
        name="activate",
    ),
    # path(
    #     "reset-password",
    #     views.ResetPasswordView.as_view(),
    #     name="reset-password",
    # ),
    # path(
    #     "confirm-reset-password/<uidb64>/<token>",
    #     views.ConfirmResetPasswordView.as_view(),
    #     name="reset-password-confirm",
    # ),
    # path("profile/", views.ShowProfile.as_view(), name="profile_show"),
    # path("profile/edit/", views.EditProfile.as_view(), name="edit_user"),
]

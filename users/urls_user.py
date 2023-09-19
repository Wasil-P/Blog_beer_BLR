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
]

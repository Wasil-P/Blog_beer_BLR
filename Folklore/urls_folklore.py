from django.urls import path

# folklore/

urlpatterns = [
    path("", name="all_folklore"),
    path("<int:folklore_id>", name="folklore_show")
]
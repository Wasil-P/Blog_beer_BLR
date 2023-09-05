from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# api/talks/
urlpatterns = [
    path("", views.CategoryTalksListAPIView.as_view()),
    path("<int:category_id>", views.OneCategoryTalksListAPIView.as_view(), name="one_category_talks_view"),
    path("<int:category_id>/<int:talks_id>", views.OneTalkListAPIView.as_view(), name="one_talk_list_view"),

    path('token/', TokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="api_token_refresh")
]
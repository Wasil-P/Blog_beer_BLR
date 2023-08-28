from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# api/
urlpatterns = [
    path("history/", views.TechnologyListAPIView.as_view(), name="all_technology_view"),
    path("history/<int:technology_id>", views.OneTechnologyAPIView.as_view(), name="one_technology_view"),
    path("my_experience/", views.ExperienceListAPIView.as_view(), name="all_experience_view"),
    path("my_experience/<int:experience_id>", views.OneExperienceAPIView.as_view(), name="one_experience_view"),
    path("talks/", views.CategoryTalksListAPIView.as_view()),
    path("talks/<int:category_id>", views.OneCategoryTalksListAPIView.as_view()),
    path("talks/<int:category_id>/<int:talks_id>", views.OneTalkListAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="api_token_refresh")
]
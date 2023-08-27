from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

# api/
urlpatterns = [
    path("history/", views.TechnologyListAPIView.as_view()),
    path("history/<int:technology_id>", views.OneTechnologyAPIView.as_view()),
    path("my_experience/", views.ExperienceListAPIView.as_view()),
    path("my_experience/<int:experience_id>", views.OneExperienceAPIView.as_view()),
    path("talks/", views.CategoryTalksListAPIView.as_view()),
    path("talks/category/", views.OneCategoryTalksListAPIView.as_view()),
    path("talks/category/<int:talks_id>", views.OneTalkListAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="api_token_refresh")
]
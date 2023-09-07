from django.urls import path
from . import views
# blog/

urlpatterns = [
    path("history/", views.TechnologiesList.as_view(), name="all_technologies"),
    path("history/<int:technology_id>", views.ShowOneTechnology.as_view(), name="technology_show"),
    path("news/", views.NewsList.as_view(), name="all_news"),
    path("news/<int:news_id>", views.ShowOneNews.as_view(), name="news_show"),
    path("my_experience/", views.ExperienceList.as_view(), name="all_experience"),
    path("my_experience/create/", views.ExperienceCreate.as_view(), name="create_experience"),
    path("my_experience/<int:experience_id>", views.ShowOneExperience.as_view(), name="experience_show"),
    path("my_experience/<int:experience_id>/edit/", views.ExperienceEdit.as_view(), name="experience_edit"),
    # path("recipes/", name="all_recipes"),
    # path("recipes/<int:recipes_id>", name="recipe_show"),
    # path("about/", name="about")
]

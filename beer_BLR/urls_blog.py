from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

# blog/

urlpatterns = [
    path("history/", cache_page(60)(views.TechnologiesList.as_view()), name="all_technologies"),
    path("history/<int:technology_id>", views.ShowOneTechnology.as_view(), name="technology_show"),
    path("news/", cache_page(60)(views.NewsList.as_view()), name="all_news"),
    path("news/<int:news_id>", views.ShowOneNews.as_view(), name="news_show"),
    path("my_experience/", cache_page(60)(views.ExperienceList.as_view()), name="all_experience"),
    path("my_experience/create/", views.ExperienceCreate.as_view(), name="create_experience"),
    path("my_experience/<int:experience_id>", views.ShowOneExperience.as_view(), name="experience_show"),
    path("my_experience/<int:experience_id>/edit/", views.ExperienceEdit.as_view(), name="experience_edit"),
    path("recipes/", cache_page(60)(views.RecipesList.as_view()), name="all_recipes"),
    path("recipes/<int:recipes_id>", views.ShowOneRecipe.as_view(), name="recipe_show"),
    path("about/", views.AboutView.as_view(), name="about")
]

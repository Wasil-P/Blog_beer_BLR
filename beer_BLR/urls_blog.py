from django.urls import path

# blog/

urlpatterns = [
    path("history/", name="all_technologies"),
    path("history/<int:technology_id>", name="technology_show"),
    path("news/", name="all_news"),
    path("news/<int:news_id>", name="news_show"),
    path("my_experience/", name="all_news"),
    path("my_experience/<int:experience_id>", name="news_show"),
    path("recipes/", name="all_recipes"),
    path("recipes/<int:recipes_id>", name="recipe_show"),
    path("about/", name="about")
]
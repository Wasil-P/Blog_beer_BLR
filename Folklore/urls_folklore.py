from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


# folklore/

urlpatterns = [
    path("", cache_page(60)(views.CategoryFolkloreList.as_view()), name="all_categories"),
    path("<int:category_id>", cache_page(60)(views.ShowOneCategory.as_view()), name="category_show"),
    path("<int:category_id>/<int:folklore_id>", views.ShowOneFolklore.as_view(), name="folklore_show"),
    path("<int:category_id>/<int:folklore_id>/comment_add/", views.CreateComment.as_view(), name="comment_add")
]
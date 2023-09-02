from django.urls import path
from . import views
# folklore/

urlpatterns = [
    path("", views.CategoryFolkloreList.as_view(), name="all_categories"),
    path("<int:category_id>", views.ShowOneCategory.as_view(), name="category_show"),
    path("<int:category_id>/<int:folklore_id>", views.ShowOneFolklore.as_view(), name="folklore_show")
]
from django.shortcuts import render, redirect, get_object_or_404, reverse
from Folklore.models import Category, Folklore, Comments
from django.views import View, generic
from django.db.models import Count, Max
from users.models import User as usermodel
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
# from .forms import PostForm, EditProfileForm
from django.db import transaction

class CategoryFolkloreList(generic.ListView):

    template_name = "Folklore/home.html"
    context_object_name = "all_categories"

    def get_queryset(self):
        return Category.objects.all().order_by("name")


class ShowOneCategory(View):
    def get_queryset(self, request, category_id):
        return Folklore.objects.filter(category__id=category_id)\
            .select_related("comments")\
            .annotate(Count("comments"))\
            .values("id", "description", "link", "comments__count")\
            .order_by("-comments__count")

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        list_folklore = self.get_queryset(request, category_id)
        return render(request, "Folklore/show_category.html",
                      {"category": category, "list_folklore": list_folklore})



class ShowOneFolklore(View):
    pass
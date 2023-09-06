from django.shortcuts import render, redirect, get_object_or_404, reverse
from Folklore.models import Category, Folklore, Comments
from django.views import View, generic
from django.db.models import Count
from django.db import transaction
from .forms import CommentsForm


class CategoryFolkloreList(generic.ListView):
    """Клас адлюстравання усіх катэгорый фальклору

        A class depicting all categories of folklore"""

    template_name = "Folklore/home.html"
    context_object_name = "all_categories"

    def get_queryset(self):
        return Category.objects.all().order_by("name")


class ShowOneCategory(View):
    """Клас адлюстравання адной катэгорыі з усімі аб'ектамі ў ёй, адлюстраванне колькасці каментароў

        A class for displaying one category with all objects in it, displaying the number of comments"""

    def get_queryset(self, request, category_id):
        return Folklore.objects.filter(category__id=category_id) \
            .select_related("comments") \
            .annotate(Count("comments")) \
            .values("id", "description", "link", "comments__count") \
            .order_by("-comments__count")

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        list_folklore = self.get_queryset(request, category_id)
        return render(request, "Folklore/show_category.html",
                      {"category": category, "list_folklore": list_folklore})


class ShowOneFolklore(View):
    """Клас адлюстравання канкрэтнага твору мастацтва з бягучымі каментарамі.

        Class rendering of a specific artwork with ongoing comments."""

    def get_queryset(self, request, folklore_id):
        return Comments.objects.filter(folklore__id=folklore_id) \
            .select_related("folklore") \
            .values("username", "content", "created", "folklore__link") \
            .order_by("-created")

    def get(self, request, category_id, folklore_id):
        category = get_object_or_404(Folklore, id=category_id)
        folklore = get_object_or_404(Folklore, id=folklore_id)
        list_comments = self.get_queryset(request, folklore_id)
        return render(request, "Folklore/folklore_show.html",
                      {"category": category, "folklore": folklore, "list_comments": list_comments})


class CreateComment(View):
    """Клас для стварэння каментароў.

    A class for creating comments."""
    model = Comments

    def get(self, request, category_id, folklore_id):
        category = get_object_or_404(Folklore, id=category_id)
        folklore = get_object_or_404(Folklore, id=folklore_id)
        return render(request, "Folklore/comment_add.html",
                      {"category": category, "folklore": folklore, "form": CommentsForm()})

    def post(self, request, category_id, folklore_id):
        form = CommentsForm(request.POST)
        folklore = get_object_or_404(Folklore, id=folklore_id)
        if not form.is_valid():
            return render(request, "Folklore/comment_add.html", {"form": form})

        with transaction.atomic():
            username = form.cleaned_data["username"]
            content = form.cleaned_data["content"]

            comments = self.model.objects.create(
                folklore=folklore,
                username=username,
                content=content,
            )
            comments.save()
        return redirect(reverse("folklore_show", kwargs={"category_id": category_id, "folklore_id": folklore_id}))

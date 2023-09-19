from django.db import transaction
from django.views import View, generic
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import Technology, News, Recipes, Experience, About
from .forms import ExperienceForm


class TechnologiesList(generic.ListView):
    """Клас адлюстравання усіх тэхналогій

        All technology mapping class"""

    template_name = "beer_BLR/technologies_home.html"
    context_object_name = "all_technologies"

    def get_queryset(self):
        return Technology.objects.all().order_by("name")


class ShowOneTechnology(View):
    """Клас адлюстравання канкрэтнай тэхналогіі

        A mapping class for a specific technology"""

    def get(self, request, technology_id):
        technology = get_object_or_404(Technology, id=technology_id)
        return render(request, "beer_BLR/show_technology.html",
                      {"technology": technology})


class NewsList(generic.ListView):
    """Клас адлюстравання усіх навін

        All news display class"""

    template_name = "beer_BLR/news_home.html"
    context_object_name = "all_news"

    def get_queryset(self):
        return News.objects.all().order_by("name")


class ShowOneNews(View):
    """Клас адлюстравання канкрэтнай навіны

        The display class of a specific news item"""

    def get_queryset(self, request, news_id):
        return News.objects.filter(id=news_id) \
            .values("id", "name", "photo", "created", "description", "tags__name") \
            .order_by("name")

    def get(self, request, news_id):
        news = self.get_queryset(request, news_id)[0]
        return render(request, "beer_BLR/show_news.html",
                      {"news": news})


class ExperienceList(generic.ListView):
    """Клас адлюстравання усіх эксперыментаў карыстальнікаў'

        A class to display all user experiments"""

    template_name = "beer_BLR/experience_home.html"
    context_object_name = "all_experience"

    def get_queryset(self):
        return Experience.objects.all().order_by("name")


class ShowOneExperience(View):
    """Клас адлюстравання адной варкі піва

        A single brew mapping class"""
    model = Experience

    def get(self, request, experience_id):
        experience = get_object_or_404(Experience, id=experience_id)
        return render(request, "beer_BLR/experience_show.html",
                      {"experience": experience})


class ExperienceCreate(View):
    """Клас для стварэння агляду эксперыментальных варак.

    A class for creating an overview of experimental brews."""
    model = Experience

    def get(self, request):
        return render(request, "beer_BLR/experience_create.html",
                      {"form": ExperienceForm()})

    def post(self, request):
        form = ExperienceForm(request.POST)

        if request.user.is_authenticated or request.user.is_staff:
            if not form.is_valid():
                return render(request, "beer_BLR/experience_create.html", {"form": form})

            with transaction.atomic():
                name = form.cleaned_data["name"]
                photo = form.cleaned_data["photo"]
                description = form.cleaned_data["description"]
                tags = form.cleaned_data["tags"]

                experience = self.model.objects.create(
                    name=name,
                    user=request.user,
                    photo=photo,
                    description=description,
                )
                experience.tags.add(*list(tags))
                experience.save()
                experience_id = experience.id

            return redirect(reverse("experience_show", kwargs={"experience_id": experience_id}))
        return redirect(reverse("register"))


class ExperienceEdit(View):
    model = Experience

    def get(self, request, experience_id):
        experience = get_object_or_404(Experience, id=experience_id)
        if experience.user == request.user or request.user.is_staff:
            return render(request, "beer_BLR/edit_experience.html", {"experience": experience, "form":
                ExperienceForm(initial={"description": experience.description, "name": experience.name})})
        return redirect(reverse("experience_show", kwargs={"experience_id": experience_id}))

    def post(self, request, experience_id):
        form = ExperienceForm(request.POST)
        experience = get_object_or_404(Experience, id=experience_id)

        if not form.is_valid():
            return render(request, "beer_BLR/edit_experience.html", {"form": form})

        with transaction.atomic():
            name = form.cleaned_data["name"]
            photo = form.cleaned_data["photo"]
            description = form.cleaned_data["description"]
            tags = form.cleaned_data["tags"]

            experience.name = name
            experience.photo = photo
            experience.description = description
            experience.tags.add(*list(tags))

            experience.save()
        return redirect(reverse("experience_show", kwargs={"experience_id": experience_id}))


class RecipesList(generic.ListView):
    """Клас адлюстравання усіх рэцэптаў традыцыйнага піва

        Class display of all traditional beer recipes"""
    template_name = "beer_BLR/recipes_home.html"
    context_object_name = "all_recipes"

    def get_queryset(self):
        return Recipes.objects.all().order_by("name")


class ShowOneRecipe(View):
    """Клас адлюстравання аднаго канкрэтнага рэцэпта

        A mapping class for one specific recipe"""
    model = Recipes

    def get(self, request, recipes_id):
        recipe = get_object_or_404(Recipes, id=recipes_id)
        return render(request, "beer_BLR/recipe_show.html",
                      {"recipe": recipe})


class AboutView(generic.ListView):
    """Клас адлюстравання інфармацыі і кантактаў аб аўтары

        A class for displaying information and contacts about the author"""

    template_name = "beer_BLR/about.html"
    context_object_name = "all_about"

    def get_queryset(self):
        return About.objects.all()


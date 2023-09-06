from django.shortcuts import render
from django.views import View, generic
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import Technology, News, Recipes, Experience, Comments, Tag, About


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
        news_ = get_object_or_404(News, id=news_id)
        news = self.get_queryset(request, news_id)[0]
        return render(request, "beer_BLR/show_news.html",
                      {"news": news, "news_": news_})

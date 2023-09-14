from django.db import transaction
from django.views import View, generic
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Count

from .models import Category, Talks, Message
from .forms import TalksForm, MessageForm


class CategoryTalksList(generic.ListView):
    """Клас адлюстравання усіх катэгорый форума

        Display class for all forum categories"""
    template_name = "Talks/talks_home.html"
    context_object_name = "all_categories"

    def get_queryset(self):
        return Category.objects.all().order_by("id")


class OneCategoryTalks(View):
    """Клас адлюстравання адной катэгорыі з усімі пытаннямі, адлюстраванне колькасці адказаў

        Display class one category with all questions, display number of answers"""

    def get_queryset(self, request, category_id):
        return Talks.objects.filter(category__id=category_id) \
            .select_related("message") \
            .annotate(Count("message")) \
            .values("id", "user", "question", "message__count") \
            .order_by("-created")

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        list_talks = self.get_queryset(request, category_id)
        return render(request, "Talks/category_show_talks.html",
                      {"category": category, "list_talks": list_talks})


class TalkCreate(View):
    """Клас для стварэння пытанняў на форуме.

    A class for creating forum questions."""
    model = Talks

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        return render(request, "Talks/talk_create.html",
                      {"category": category, "form": TalksForm()})

    def post(self, request, category_id):
        form = TalksForm(request.POST)
        category = get_object_or_404(Category, id=category_id)

        if not form.is_valid():
            return render(request, "Talks/talk_create.html", {"form": form})

        with transaction.atomic():
            question = form.cleaned_data["question"]

            talk = self.model.objects.create(
                category=category,
                user=request.user,
                question=question
            )
            talk.save()
            talk_id = talk.id

        return redirect(reverse("talk_show", kwargs={"category_id": category_id, "talk_id": talk_id}))


class TalkEdit(View):
    """Клас для рэдагаванне пытання ўласнікам, ці адміністратарам.

    A class for editing a question by the owner or administrator."""
    model = Talks

    def get(self, request, category_id, talk_id):
        talk = get_object_or_404(Talks, id=talk_id)
        category = get_object_or_404(Category, id=category_id)
        return render(request, "Talks/edit_talk.html", {"category": category, "talk": talk, "form":
            TalksForm(initial={"question": talk.question})})

    def post(self, request, category_id, talk_id):
        form = TalksForm(request.POST)
        talk = get_object_or_404(Talks, id=talk_id)
        category = get_object_or_404(Category, id=category_id)

        if not form.is_valid():
            return render(request, "Talks/edit_talk.html", {"form": form})

        with transaction.atomic():
            question = form.cleaned_data["question"]

            talk.question = question

            talk.save()
        return redirect(reverse("talk_show", kwargs={"category_id": category_id, "talk_id": talk_id}))


class OneTalkShow(View):
    """Клас адлюстравання аднаго пытання, адказы карыстальнікаў на пытанне

        A class representing a single question, user responses to a question"""

    def get_queryset(self, request, talk_id):
        return Message.objects.filter(talks__id=talk_id) \
            .select_related("user", "talks") \
            .values("user", "created", "description", "user__username", "talks__category__name") \
            .order_by("-created")

    def get(self, request, category_id, talk_id):
        category = get_object_or_404(Category, id=category_id)
        talk = get_object_or_404(Talks, id=talk_id)
        list_message = self.get_queryset(request, talk_id)
        return render(request, "Talks/talk_show.html",
                      {"category": category, "talk": talk, "list_message": list_message})


class MessageCreate(View):
    """Клас для стварэння адказаў на пытанні на форуме зарэгістраванымі карыстальнікамі.

    A class for creating responses to forum questions by registered users."""
    model = Message

    def get(self, request, category_id, talk_id):
        category = get_object_or_404(Category, id=category_id)
        talk = get_object_or_404(Talks, id=talk_id)
        return render(request, "Talks/message_add.html",
                      {"category": category, "talk": talk, "form": MessageForm()})

    def post(self, request, category_id, talk_id):
        form = MessageForm(request.POST)
        talk = get_object_or_404(Talks, id=talk_id)
        if not form.is_valid():
            return render(request, "Talks/message_add.html", {"form": form})

        with transaction.atomic():
            description = form.cleaned_data["description"]

            message = self.model.objects.create(
                talks=talk,
                user=request.user,
                description=description,
            )
            message.save()
        return redirect(reverse("talk_show", kwargs={"category_id": category_id, "talk_id": talk_id}))


import textwrap
from django.contrib import admin

from .models import Talks, Message


@admin.register(Talks)
class TalksAdmin(admin.ModelAdmin):
    list_display = ["user", "created_views", "category", "question_short"]
    search_fields = ["user", "created"]
    list_filter = ["category", "user"]


    @admin.display(description="Question")
    def question_short(self, obj: Talks):
        if len(obj.question)>30:
            return textwrap.wrap(obj.question, 30)[0] + "..."
        return obj.question

    @admin.display(description="Created")
    def created_views(self, obj: Talks):
        data = obj.created.strftime('%d.%m.%Y %H:%M')
        return data


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["talks_short", "user", "created_views", "description_short"]
    search_fields = ["user"]
    list_filter = ["talks", "user"]


    @admin.display(description="Talks")
    def talks_short(self, obj: Message):
        if len(obj.talks.question)>25:
            return textwrap.wrap(obj.talks.question, 25)[0] + "..."
        return obj.talks.question

    @admin.display(description="Description")
    def description_short(self, obj: Message):
        if len(obj.description)>25:
            return textwrap.wrap(obj.description, 25)[0] + "..."
        return obj.description

    @admin.display(description="Created")
    def created_views(self, obj: Message):
        data = obj.created.strftime('%d.%m.%Y %H:%M')
        return data

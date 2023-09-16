import textwrap
from django.utils.html import format_html
from django.contrib import admin

from .models import News, Experience


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["name", "photo", "created_views", "description_short", "tags_all"]
    search_fields = ["name", "created"]
    list_filter = ["tags", "created"]
    actions = ["delete_teg_all"]

    @admin.display(description="Тags")
    def tags_all(self, obj: News):
        tags_all = obj.tags.all().values_list("name", flat=True)
        rest_list = [f"<li>{tag_name}</li>"for tag_name in tags_all]
        return format_html("".join(rest_list))

    @admin.display(description="Description")
    def description_short(self, obj: News):
        if len(obj.description)>50:
            return textwrap.wrap(obj.description, 50)[0] + "..."
        return obj.description

    @admin.display(description="Created")
    def created_views(self, obj: News):
        data = obj.created.strftime('%d.%m.%Y %H:%M')
        return data

    @admin.action(description="Выдаліць усе тэгі")
    def delete_teg_all(self, form, queryset):
        for obj in queryset:
            obj.tags.clear()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "description_short", "tags_all"]
    search_fields = ["name", "user"]
    list_filter = ["tags", "user"]
    actions = ["delete_teg_all"]

    @admin.display(description="Тags")
    def tags_all(self, obj: Experience):
        tags_all = obj.tags.all().values_list("name", flat=True)
        rest_list = [f"<li>{tag_name}</li>"for tag_name in tags_all]
        return format_html("".join(rest_list))

    @admin.display(description="Description")
    def description_short(self, obj: Experience):
        if len(obj.description)>50:
            return textwrap.wrap(obj.description, 50)[0] + "..."
        return obj.description

    @admin.action(description="Выдаліць усе тэгі")
    def delete_teg_all(self, form, queryset):
        for obj in queryset:
            obj.tags.clear()

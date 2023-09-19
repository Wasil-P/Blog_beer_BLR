import textwrap
from django.contrib import admin

from .models import Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["folklore_short", "username", "content_short", "created_views"]
    search_fields = ["username", "created"]
    list_filter = ["username", "created"]


    @admin.display(description="Folklore")
    def folklore_short(self, obj: Comments):
        if len(obj.folklore.description)>25:
            return textwrap.wrap(obj.folklore.description, 25)[0] + "..."
        return obj.folklore.description

    @admin.display(description="Content")
    def content_short(self, obj: Comments):
        if len(obj.content)>30:
            return textwrap.wrap(obj.content, 30)[0] + "..."
        return obj.content

    @admin.display(description="Created")
    def created_views(self, obj: Comments):
        data = obj.created.strftime('%d.%m.%Y %H:%M')
        return data



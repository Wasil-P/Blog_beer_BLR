from django.views import generic

from .models import Menu


class MenuList(generic.ListView):
    """Клас адлюстравання усяго меню

        The entire menu display class"""

    template_name = "Menu/Menu.html"
    context_object_name = "menu_links"

    def get_queryset(self):
        return Menu.objects.all().order_by("id")


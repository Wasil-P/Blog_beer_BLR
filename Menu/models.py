from django.db import models


class Menu(models.Model):
    """Клас для адлюстравання галоўнага меню усяго блога.

    A class to display the main menu of the entire blog.
    """
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    class Meta:
        db_table = "Menu"

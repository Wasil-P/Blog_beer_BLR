from django.db import models


class Category(models.Model):
    """Мадэль для катэгорыі (віда) твора фальклору

    A model of a category (type) of a folklore work"""
    # PROVERB = "Proverb"
    # RIDDLE = "Riddle"
    # SONG = "Song, an excerpt of a song"
    # RITE = "Rite"
    name = models.CharField(max_length=100)


class Folklore(models.Model):
    """Мадэль для адлюстравання твораў фальклору, урыўкаў
    field link: спасылка на папяровае, ці інтэрнэт-выданне

    Model for viewing works of folklore, excerpts
      field link: a link to a paper or online publication"""
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="folklore")
    description = models.TextField(max_length=10_000)
    link = models.TextField(max_length=256)


class Comments(models.Model):
    """Мадэль для каментара пад творамі фальклору

    Model for comments under works of folklore"""
    folklore = models.ForeignKey(Folklore, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created.strftime('%d.%m.%Y %H:%M')

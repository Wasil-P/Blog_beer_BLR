from django.db import models
# from ya_storage.storage import yandex_disk_storage


class Technology(models.Model):
    """У дадзенай мадэлі апісаныя непасрэдныя традыцыйныя тэхналогіі піваварэння,
    якія былі зафіксаваныя на тэрыторыі Беларусі.
    field location: спасылка на гуглкарту, з канкрэтным месцазнаходжаннем зафіксаванай тэхналогіі

    This model describes direct traditional brewing technologies,
     which were recorded on the territory of Belarus.
     field location: a link to a Google map with the specific location of the recorded technology
    """
    name = models.CharField(max_length=100)
    # Пакуль не ведаю, як гэта рэалізаваць
    # location = models.LocationField()
    photo = models.ImageField(null=True, upload_to="history/")
    description = models.TextField(max_length=10_000)

    class Meta():
        db_table = "technologies"


class News(models.Model):
    """У дадзенай мадэлі апісанне навіны для блога

    In this model, the description of the news for the blog"""
    name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, upload_to="blog/")
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=5_000)
    tags = models.ManyToManyField("Tag", related_name="news")

    def __str__(self):
        return self.created.strftime('%d.%m.%Y %H:%M')

class Recipes(models.Model):
    """У дадзенай мадэлі апісанне рэцэпта піва канкрэтнай тэхналогіі

    This model describes the beer recipe of a specific technology"""
    name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, upload_to="recipes/")
    description = models.TextField(max_length=5_000)


class Experience(models.Model):
    """У дадзенай мадэлі апісаны вопыт варкі піва па традыцыйнаму рэцэпту канкрэтнага карыстальніка.

    This model describes the experience of brewing beer according to a traditional recipe of a specific user."""
    name = models.CharField(max_length=100)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="experience_user")
    photo = models.ImageField(null=True, upload_to="my_ experience/")
    description = models.TextField(max_length=5_000)
    tags = models.ManyToManyField("Tag", related_name="experience_tags")


    class Meta():
        db_table = "experiences"


class Comments(models.Model):
    """Мадэль для каментара пад пастамі з вопытам варак канкрэтнага карыстальніка

    A model for commenting posts with a specific user's brewing experience"""
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created.strftime('%d.%m.%Y %H:%M')


class Tag(models.Model):
    name = models.CharField(max_length=20)


class About(models.Model):
    """Мадэль для азнаямлення карыстальнікаў з аўтарам блога

    A model for introducing users to the author of a blog"""
    profile_picture = models.ImageField(null=True)
    description = models.TextField(max_length=500)
    email = models.EmailField()
    insta = models.CharField(max_length=100)

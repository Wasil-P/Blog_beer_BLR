from django.db import models
from django.utils.html import escape
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Мадэль для стварэння карыстальнікаў
       field notify: поле падцвярджэння для далейшай рассылкі навінаў, адказаў на пытанні і інш"""
    email = models.EmailField(null=False)
    profile_picture = models.ImageField(null=True)
    notify = models.BooleanField(default=True)
    tg_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "users"


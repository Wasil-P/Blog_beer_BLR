from django.db import models


class Category(models.Model):
    """Мадэль для катэгорыі пытанняў карыстальнікаў

    A model that describes categories for user questions"""
    name = models.CharField(max_length=100)


class Talks(models.Model):
    """Мадэль, якая апісвае пытанні ўнесеныя на форуме ад зарэгістраваных карыстальнікаў
    field question: пытанне канкрэтнага карыстальніка

    A model that describes questions submitted to the forum by registered users
          question field: The content of the user's question"""
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="talks_user")
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="talks_category")
    question = models.TextField(max_length=500)


class Message(models.Model):
    """Мадэль для адказаў карыстальнікаў на форуме

    Model for forum user responses"""
    talks = models.ForeignKey(Talks, on_delete=models.CASCADE, related_name="message")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="message_user")
    description = models.TextField(max_length=1000)


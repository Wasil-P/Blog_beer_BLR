from django import forms

from .models import Talks, Message


class TalksForm(forms.ModelForm):

    class Meta:
        model = Talks
        fields = ["question"]


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["description"]

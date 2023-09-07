from django import forms

from .models import Experience


class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ["name", "photo", "description", "tags"]


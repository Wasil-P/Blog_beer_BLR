from rest_framework import serializers
from ..models import Technology, Experience
from Talks.models import Talks, Category, Message


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:

        model = Technology
        fields = ['name', 'description']
        read_only_fields = ['location', 'photo']


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ['name', 'user', 'description', 'tags']
        read_only_fields = ['profile_picture', 'photo']


class CategoryTalksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class OneCategoryTalksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talks
        fields = ['category', 'question', 'created', 'user']
        read_only_fields = ['message']


class OneTalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['talks', 'description', 'created', 'user']

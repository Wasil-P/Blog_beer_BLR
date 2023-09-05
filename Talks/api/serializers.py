from rest_framework import serializers
from ..models import Talks, Category, Message


class CategoryTalksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class OneCategoryTalksSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Talks
        fields = ['category', 'question', 'created', 'user']
        read_only_fields = ['message']


class OneTalkSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    talks = serializers.CharField(source="talks.question")

    class Meta:
        model = Message
        fields = ['talks', 'description', 'created', 'user']

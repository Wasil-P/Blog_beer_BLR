from rest_framework import serializers
from ..models import Technology, Experience


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:

        model = Technology
        fields = ['name', 'description']
        read_only_fields = ['location', 'photo']


class ExperienceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Experience
        fields = ['name', 'user', 'description', 'tags']
        read_only_fields = ['profile_picture', 'photo']



from rest_framework.test import APITestCase
from rest_framework import status
from django.shortcuts import reverse

from users.models import User
from Talks.models import Talks, Category, Message
from ..models import Experience


class TestAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        superuser = {"username": "superuser",
                     "password": "123",
                     "email": "superuser@mail.com"}

        user_owner = {"username": "user_owner",
                      "password": "321",
                      "email": "user_owner@mail.com"}

        user = {"username": "user",
                "password": "4321",
                "email": "user@mail.com"}

        User.objects.create_user(is_staff=True, **superuser)
        User.objects.create_user(**user_owner)
        User.objects.create_user(**user)

        user_own = User.objects.get(username='user_owner')

        cls.superuser = superuser
        cls.user_owner = user_owner
        cls.user = user

        experience = {"name": "my_beer",
                      "user": user_own,
                      "description": "historycal_beer"}

        cls.experience = Experience.objects.create(**experience)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.superuser_tokens = self.client.post("/api/token/", self.superuser).json()
        self.user_owner_tokens = self.client.post("/api/token/", self.user_owner).json()
        self.user_tokens = self.client.post("/api/token/", self.user).json()
from rest_framework.test import APITestCase
from rest_framework import status
from django.shortcuts import reverse

from users.models import User
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
        user_ = User.objects.get(username='user')

        cls.superuser = superuser
        cls.user_owner = user_owner
        cls.user = user

        experience = {"name": "my_beer",
                      "user": user_own,
                      "description": "historycal_beer"}

        cls.experience = Experience.objects.create(**experience)

        experience_2 = {"name": "my_beer",
                      "user": user_,
                      "description": "historycal_beer"}

        cls.experience_2 = Experience.objects.create(**experience_2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.superuser_tokens = self.client.post("/api/blog/token/", self.superuser).json()
        self.user_owner_tokens = self.client.post("/api/blog/token/", self.user_owner).json()
        self.user_tokens = self.client.post("/api/blog/token/", self.user).json()

    """Праверка прагляду ўсіх варак юзэраў. Праверка магчымасці стварыць зарэгістраванымі юзэрамі 
    эксперымантальных варак
    
    Checking the view of all users' brews. Checking the ability to create by registered users
     experimental brews"""

    def test_all_and_create_experience_view(self):
        # Get method without authorization
        user = User.objects.get(username='user')
        resp = self.client.get(reverse("all_experience_view"))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method Post authorized user
        resp = self.client.post(reverse("all_experience_view"),
                                HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                data={
                                    "name": "user_beer",
                                    "user": user.id,
                                    "description": "historycal_beer"},
                                format='json'
                                )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method Post without authorization
        resp = self.client.post(reverse("all_experience_view"),
                                data={
                                    "name": "New2",
                                    "user": "user_not_authorization",
                                    "description": "old2_technology"}
                                )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    """Праверка прагляду аднаго эксперымента. Праверка магчымасці рэдагаваць адмінам  і 
    зарэгістраваным юзэрам-уласнікам варку.
    
    Checking the view of a single experiment. Checking the ability to edit admin and
     registered user-owner of the brew."""

    def test_one_experience_view(self):
        # Get method without authorization
        resp = self.client.get(reverse("one_experience_view", args=(self.experience.id,)))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method patch authorized user_not_owner
        resp = self.client.patch(reverse("one_experience_view", args=(self.experience.id,)),
                                 HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                 data={
                                     "name": "New1"}
                                 )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Method patch authorized user_owner
        resp = self.client.patch(reverse("one_experience_view", args=(self.experience.id,)),
                                 HTTP_AUTHORIZATION=f"Bearer {self.user_owner_tokens.get('access')}",
                                 data={
                                     "name": "New2"}
                                 )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method patch Admin
        resp = self.client.patch(reverse("one_experience_view", args=(self.experience.id,)),
                                 HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}",
                                 data={
                                     "name": "New3"}
                                 )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method delete authorized user_not_owner
        resp = self.client.delete(reverse("one_experience_view", args=(self.experience.id,)),
                                  HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                  )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Method delete authorized user_owner
        resp = self.client.delete(reverse("one_experience_view", args=(self.experience.id,)),
                                  HTTP_AUTHORIZATION=f"Bearer {self.user_owner_tokens.get('access')}",
                                  )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # Method delete authorized Admin
        resp = self.client.delete(reverse("one_experience_view", args=(self.experience_2.id,)),
                                  HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}",
                                  )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

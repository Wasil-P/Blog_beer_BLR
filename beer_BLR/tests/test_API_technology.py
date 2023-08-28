from rest_framework.test import APITestCase
from rest_framework import status
from django.shortcuts import reverse

from users.models import User
from ..models import Technology


class TestAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        superuser = {"username": "superuser",
                     "password": "123",
                     "email": "superuser@mail.com"}

        user = {"username": "user",
                "password": "321",
                "email": "user@mail.com"}

        User.objects.create_user(is_staff=True, **superuser)
        User.objects.create_user(**user)

        cls.superuser = superuser
        cls.user = user

        technology = {"name": "samahodskae",
                      "description": "piwa_belarusau_sibiry"}

        cls.technology = Technology.objects.create(**technology)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.superuser_tokens = self.client.post("/api/token/", self.superuser).json()
        self.user_tokens = self.client.post("/api/token/", self.user).json()

    """Праверка прагляду ўсіх тэхналогій. Праверка магчымасці стварыць адмінам тэхналогію
    Checking the view of a single technology. Checking the ability to create a technology adminuser"""

    def test_all_and_create_technology_view(self):
        # Get method without authorization
        resp = self.client.get(reverse("all_technology_view"))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method Post authorized normal user
        resp = self.client.post(reverse("all_technology_view"),
                                HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                data={
                                    "name": "New1",
                                    "description": "old1_technology"}
                                )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Method Post authorized Admin
        resp = self.client.post(reverse("all_technology_view"),
                                HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}",
                                data={
                                    "name": "New2",
                                    "description": "old2_technology"}
                                )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    """Праверка прагляду адной тэхналогіі. Праверка магчымасці рэдагаваць адмінам тэхналогіі
    Checking the view of a single technology. Possibility of admin editing a technology"""

    def test_one_technology_view(self):
        # Get method without authorization
        resp = self.client.get(reverse("one_technology_view", args=(self.technology.id,)))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method patch authorized normal user
        resp = self.client.patch(reverse("one_technology_view", args=(self.technology.id,)),
                                 HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                 data={
                                     "name": "New1",
                                     "description": "one_technology"}
                                 )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Method patch authorized Admin
        resp = self.client.patch(reverse("one_technology_view", args=(self.technology.id,)),
                                 HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}",
                                 data={
                                     "name": "New2",
                                     "description": "two_technology"}
                                 )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method delete authorized normal user
        resp = self.client.delete(reverse("one_technology_view", args=(self.technology.id,)),
                                  HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                  )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Method delete authorized Admin
        resp = self.client.delete(reverse("one_technology_view", args=(self.technology.id,)),
                                  HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}",
                                  )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

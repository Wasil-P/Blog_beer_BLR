from rest_framework.test import APITestCase
from rest_framework import status
from django.shortcuts import reverse
import datetime

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

        category = {"name": "Water"}
        category_ = Category.objects.create(**category)
        category_id = Category.objects.get(name='Water')

        created = datetime.datetime.now()
        talk = {"user": user_own,
                "created": created,
                "category": category_id,
                "question": "Who?"}
        talk_ = Talks.objects.create(**talk)
        talk_id = Talks.objects.get(question='Who?')

        message = {"talks": talk_id,
                   "user": user_own,
                   "created": created,
                   "description": "Everybody"}
        message_ = Message.objects.create(**message)

        cls.category = category_
        cls.category_id = category_id
        cls.created = created
        cls.talks = talk_
        cls.message = message_

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.superuser_tokens = self.client.post("/api/token/", self.superuser).json()
        self.user_owner_tokens = self.client.post("/api/token/", self.user_owner).json()
        self.user_tokens = self.client.post("/api/token/", self.user).json()

    """Праверка магчымасці прагляду усіх пытанняў ад карыстальнікаў па канкрэтнай катэгорыі.
    Магчымасць ствараць новыя пытанні па канкрэтнай катэгорыі зарэгістраваным юзэрам
    
    Check the possibility of viewing all questions from users in a specific category. 
    The ability to create new questions in a specific category is available to registered users."""

    def test_one_category_talks_view(self):
        # Get method without authorization
        resp = self.client.get(reverse("one_category_talks_view", args=(self.category.id,)))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Method Post without authorization
        user = User.objects.get(username='user')
        resp = self.client.post(reverse("one_category_talks_view", args=(self.category.id,)),
                                data={
                                    "user": user.id,
                                    "created": self.created,
                                    "category": self.category_id,
                                    "question": "Where?"})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Method Post authorized user
        user = User.objects.get(username='user')
        resp = self.client.post(reverse("one_category_talks_view", args=(self.category.id,)),
                                HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
                                data={
                                    "user": user.id,
                                    "created": self.created,
                                    "category": self.category_id,
                                    "question": "Where?"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    """Праверка прагляду адказаў па каанкрэтнаму пытанню. Праверка магчымасці стварэння і
    рэдагавання адказаў зарэгістраванымі юзэрамі
    
    Check the answer view for a specific question. Checking the ability to create and
     editing of answers by registered users"""
    def test_one_talk_list_view(self):
        # Get method without authorization

        resp = self.client.get("one_category_talks_view",
                               kwargs={"category_id": self.category.id, "talks_id": self.talks.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

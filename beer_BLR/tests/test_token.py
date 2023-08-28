from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status


class TestJWTAuth(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(
            username="username",
            password="567gjtfi7yuilgh78",
            email="user@mail.com",
        )
        print(cls.user)
        print(type(cls.user))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        """Праверка атрымання access- и refresh- токена
            Checking access and refresh token receipt"""
    def test_get_token_valid(self):
        resp = self.client.post("/api/token/",
                                data={
                                        "username": self.user.username,
                                        "password": "567gjtfi7yuilgh78",
                                    })

        data = resp.json()
        print(data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    """Праверка адсутнасці магчымасці атрымаць токен з неправільнымі дадзенымі і без іх
        An absence check will receive a token with and without invalid attributions"""
    def test_get_token_invalid(self):
        resp = self.client.post("/api/token/",
                                data={
                                    "username": self.user.username,
                                    "password": "1",
                                })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        resp = self.client.post("/api/token/",
                                data={
                                    "username": self.user.username,
                                })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post("/api/token/",
                                data={
                                    "password": "567gjtfi7yuilgh78",
                                })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """Праверка атрымання новага access-токена
        Checking for a new access token"""
    def test_get_token_refresh(self):
        resp = self.client.post("/api/token/",
                                data={
                                        "username": self.user.username,
                                        "password": "567gjtfi7yuilgh78",
                                    })

        data = resp.json()
        print(f'first_data - {data}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        refresh_token = resp.json()["refresh"]
        print(f'first_refresh - {refresh_token}')

        resp = self.client.post("/api/token/refresh/",
                                data={"refresh": refresh_token})
        print(f"new_access - {resp.json()}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.json())


from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


def user_url():
    return reverse("user:user_register")


def user_me_url():
    return reverse("user:user_me")


class UserTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_new_user_success(self):
        payload = {
            "email": "new_user@gmail.com",
            "password": "PASSWORD",
        }
        result = self.client.post(user_url(), payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)


class UserAuthenticatedTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@gmail.com",
            password="PASSWORD",
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticate_user_get_profile(self):
        result = self.client.get(user_me_url())
        self.assertEqual(result.status_code, status.HTTP_200_OK)


class UserUnauthenticatedTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_get_profile(self):
        result = self.client.get(user_me_url())
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

from django.test import TestCase
from django.urls import reverse


class LoginViewTestCase(TestCase):
    def test_post_login(self):
        data = {
            "username": "john",
            "password1": "qWeRtY123!"
        }
        response = self.client.post(reverse('myauth:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.path, reverse('myauth:about-me'))


class SignUpViewTestCase(TestCase):
    def test_post_signup(self):
        data = {
            "username": "john1",
            "password1": "qWeRtY123!"
        }
        response = self.client.post(reverse('myauth:signup'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.path, reverse('myauth:about-me'))

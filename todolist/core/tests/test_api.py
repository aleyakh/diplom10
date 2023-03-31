import json

from rest_framework.test import APITestCase
from django.test import Client
from todolist.core.models import User


class CoreApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.user = User.objects.create_user(username='test_user', password='test', is_superuser=True)
        cls.c = Client()
        # cls.response = cls.c.login(username='test_user', password='test')

    def create_user(self):
        password = 'test1111'
        user = User.objects.create_user(username='test_user', password=password)
        return user, password

    def test_signup(self):
        url = '/core/signup'
        response = self.c.post(url, {'username': 'test_user', 'password': 'test1111', 'password_repeat': 'test1111'})
        # print(response)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        user, password = self.create_user()
        # print(user, user.username, password)
        url = '/core/login'

        response = self.c.post(url, {'username': user.username, 'password': password})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('username'), user.username)

    def test_profile_get(self):
        user, password = self.create_user()
        self.c.login(username=user, password=password)

        url = "/core/profile"

        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), user.id)

    def test_profile_put(self):
        user, password = self.create_user()
        self.c.login(username=user, password=password)
        url = "/core/profile"
        first_name = 'TEST'
        response = self.c.put(url, json.dumps({'username': user.username, 'first_name': first_name}), content_type='application/json')
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=user.id).first_name, first_name)

    def test_update_password(self):
        user, password = self.create_user()
        self.c.login(username=user, password=password)

        url = "/core/update_password"

        new_password = "test2222"
        response = self.c.put(url, json.dumps({'old_password': password, 'new_password': new_password}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        logged_in = self.c.login(username=user.username, password=new_password)
        self.assertTrue(logged_in)





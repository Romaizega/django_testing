from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Чтец')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='slug'
        )
        cls.home_url = reverse('notes:home', None)
        cls.login_url = reverse('users:login', None)
        cls.logout_url = reverse('users:logout', None)
        cls.signup_url = reverse('users:signup', None)
        cls.list_url = reverse('notes:list', None)
        cls.success_url = reverse('notes:success', None)
        cls.add_url = reverse('notes:add', None)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

    def test_home_pages_availability_for_annonim_user(self):
        urls = (
            self.home_url,
            self.login_url,
            self.logout_url,
            self.signup_url,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_home_pages_availability_for_auth_user(self):
        urls = (
            self.list_url,
            self.success_url,
            self.add_url,
        )
        self.client.force_login(self.author)
        for page in urls:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_comment_edit_and_delete(self):
        urls = (
            self.detail_url,
            self.edit_url,
            self.delete_url,
        )
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for page in urls:
                with self.subTest(user=user, page=page):
                    response = self.client.get(page)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_annonim_client(self):
        login_url = reverse('users:login')
        urls = (
            self.add_url,
            self.list_url,
            self.success_url,
            self.edit_url,
            self.detail_url,
            self.delete_url,
        )
        for name in urls:
            with self.subTest():
                redirect_url = f'{login_url}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)

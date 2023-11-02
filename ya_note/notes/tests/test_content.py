from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note
from django.urls import reverse

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Чтец')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )
        cls.add_url = reverse('notes:add')

    def test_note_visibl_for_author(self):
        url = reverse('notes:list')
        user = self.author
        self.client.force_login(user)
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_visibl_for_reader(self):
        url = reverse('notes:list')
        user = self.reader
        self.client.force_login(user)
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_edit_form(self):
        user = self.author
        self.client.force_login(user)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)

    def test_add_form(self):
        user = self.author
        self.client.force_login(user)
        response = self.client.get(self.add_url)
        self.assertIn('form', response.context)

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):
    URL_LIST = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Чтец')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='Slug'
        )
        cls.add_url = reverse('notes:add')

    def test_note_visibility(self):
        users = (
            (self.author, self.assertIn),
            (self.reader, self.assertNotIn)
        )

        for user, viss_assert in users:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(self.URL_LIST)
                object_list = response.context['object_list']
                viss_assert(self.note, object_list)

    def test_edit_add_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for user, args in urls:
            with self.subTest(user=user):
                self.client.force_login(self.author)
                response = self.client.get(reverse(user, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

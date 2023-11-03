from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    TEXT_OF_THE_NOTE = 'Текст'
    TITLE_OF_THE_NOTE = 'Заголовок'
    SLUG_OF_THE_NOTE = 'slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Чтец')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.form_data = {'text': cls.TEXT_OF_THE_NOTE,
                         'title': cls.TITLE_OF_THE_NOTE,
                         'slug': cls.SLUG_OF_THE_NOTE}
        cls.url_for_add = reverse('notes:add')

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(
            self.url_for_add, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.TEXT_OF_THE_NOTE)
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.SLUG_OF_THE_NOTE)

    def test_annonim_user_cant_create_note(self):
        response = self.client.post(
            self.url_for_add,
            data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.url_for_add}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.url_for_add,
            data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestSlugEDitDeletNote(TestCase):
    TEXT_OF_THE_NOTE = 'Текст'
    TITLE_OF_THE_NOTE = 'Заголовок'
    SLUG_OF_THE_NOTE = 'slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title='title',
            text='text',
            author=cls.author,
            slug='no_slug')
        cls.url_for_add = reverse('notes:add')
        cls.url_for_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_for_delete = reverse('notes:delete',
                                     args=(cls.note.slug,))
        cls.form_data = {'text': cls.TEXT_OF_THE_NOTE,
                         'title': cls.TITLE_OF_THE_NOTE,
                         'slug': cls.SLUG_OF_THE_NOTE}
        cls.reader = User.objects.create(username='Чтец')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.url_for_add,
                                           data=self.form_data)
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.note.slug + WARNING))
        self.assertEqual(Note.objects.count(), 1)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.url_for_edit, self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.slug, self.form_data['slug'])
        self.assertEqual(self.note.text, self.form_data['text'])

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(self.url_for_edit, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.text, note_from_db.text)

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.url_for_delete)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), Note.objects.count())

    def test_other_user_cant_delete_note(self):
        response = self.reader_client.post(self.url_for_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)

import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonimus_cant_post_comment(client, form_data, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_redirect = f'{login_url}?next={url}'
    assertRedirects(response, expected_redirect)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_create_comment(author, author_client, form_data, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    comment = Comment.objects.first()

    assert response.status_code == HTTPStatus.FOUND
    assert comments_count == 1
    assert comment.news == news
    assert comment.author == author
    assert comment.text == form_data['text']
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_users_cant_use_badwords_(author_client, news):
    bad_words_text = {'text': f' Текст, {BAD_WORDS[0]}, и еще текст'}
    comment_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_words_text)
    assert response.context['form'].errors.get('text') == [WARNING]
    assert comment_count == 0


@pytest.mark.django_db
def test_author_can_edit_comment(
        author, author_client, news, comment, form_data,):
    edit_url = reverse('news:edit', args=(comment.id,))
    url = reverse('news:detail', args=(news.id,))
    url_to_comments = url + '#comments'
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_author_delete_comment(author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.post(delete_url)
    comment_exists = Comment.objects.filter(pk=comment.id).exists()
    assert response.status_code == HTTPStatus.FOUND
    assert not comment_exists


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
        author, admin_client, news, comment, form_data):
    comment_text = comment.text
    edit_url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(edit_url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


def test_user_can_delete_comment(admin_client, comment):
    comment_count_first = Comment.objects.count()
    delete_url = reverse('news:delete', args=(comment.id,))
    response = admin_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count_last = Comment.objects.count()
    assert comment_count_first == comment_count_last

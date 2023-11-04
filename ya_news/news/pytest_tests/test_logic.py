from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment
from news.forms import WARNING


@pytest.mark.django_db
def test_anonimus_cant_post_comment(
        client,
        form_data,
        url_detail,
        url_login
):
    response = client.post(url_detail, data=form_data)
    expected_redirect = f'{url_login}?next={url_detail}'
    assertRedirects(response, expected_redirect)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_auth_user_can_create_comment(
        author,
        author_client,
        form_data,
        news,
        url_detail
):
    response = author_client.post(url_detail, data=form_data)
    comments_count = Comment.objects.count()
    comment = Comment.objects.first()

    assert response.status_code == HTTPStatus.FOUND
    assert comments_count == 1
    assert comment.news == news
    assert comment.author == author
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_users_cant_use_badwords_(
        bad_words_text,
        author_client,
        url_detail
):
    response = author_client.post(url_detail, data=bad_words_text)
    assertFormError(response, 'form', 'text', [WARNING])
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(
        author,
        author_client,
        news,
        comment,
        form_data,
        url_edit,
        url_detail
):
    url_to_comments = url_detail + '#comments'
    response = author_client.post(url_edit, form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_author_delete_comment(author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.post(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(pk=comment.id).exists()


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
        author,
        admin_client,
        news,
        comment,
        form_data,
        url_edit,
):
    comment_text = comment.text
    response = admin_client.post(url_edit, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


def test_user_cant_delete_comment(admin_client, comment, url_delete):
    response = admin_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == Comment.objects.count()

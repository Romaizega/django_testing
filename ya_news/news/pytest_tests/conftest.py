from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.test import Client

from news.forms import BAD_WORDS
from news.models import Comment, News


@pytest.fixture
def author():
    User = get_user_model()
    return User.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader():
    User = get_user_model()
    return User.objects.create(username='Чтец')


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст',
        date=timezone.now()
    )


@pytest.fixture
def create_news():
    news_list = []
    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        news = News.objects.create(
            title='title',
            text='text {index}',
            date=timezone.now() + timedelta(days=i)
        )
        news_list.append(news)
    return len(news_list)


@pytest.fixture
def create_comment(author, news):
    now = timezone.now()
    for i in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Test commen {i}',
        )
        comment.created = now + timedelta(days=i)
        comment.save()


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Test comment',
    )


@pytest.fixture
def comment_id(comment):
    return (comment.id),


@pytest.fixture
def form_data():
    return {
        'title': 'Test title',
        'text': 'Test text',
    }


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def bad_words_text():
    return {'text': f' Текст, {BAD_WORDS[0]}, и еще текст'}

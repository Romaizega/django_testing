import pytest

from news.forms import CommentForm
from django.conf import settings

pytestmark = pytest.mark.django_db


def test_news_count(client, url_home, create_news):
    response = client.get(url_home)
    object_list = response.context.get('object_list')
    assert object_list is not None
    assert len(object_list) <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_sorted(client, url_home, create_news):
    response = client.get(url_home)
    object_list = response.context.get('object_list')
    assert object_list is not None
    dates = [create_news.date for create_news in object_list]
    assert sorted(dates, reverse=True) == dates


def test_comments_sorted(client, create_comment, url_detail):
    response = client.get(url_detail)
    news = response.context.get('news')
    assert news is not None
    all_comments = news.comment_set.all()
    dates = [comment.created for comment in all_comments]
    assert dates == sorted(dates)


@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('admin_client'), True),
    ),
)
def test_form_for_user_on_deteil(
        parametrized_client,
        form_in_context,
        url_detail,
):
    response = parametrized_client.get(url_detail)
    have_form = 'form' in response.context
    assert have_form is form_in_context
    if have_form:
        assert isinstance(response.context.get('form'), CommentForm)

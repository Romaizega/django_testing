import pytest

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, url_home, fixt_news_count):
    response = client.get(url_home)
    object_list = response.context.get('object_list')
    assert len(object_list) <= fixt_news_count


def test_news_sorted(client, url_home):
    response = client.get(url_home)
    object_list = response.context.get('object_list')
    dates = [new.date for new in object_list]
    assert sorted(dates, reverse=True) == dates


def test_comments_sorted(client, news, url_detail):
    response = client.get(url_detail)
    news = response.context['news']
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
        news,
        parametrized_client,
        form_in_context,
        url_detail,
):
    response = parametrized_client.get(url_detail)
    have_form = 'form' in response.context
    assert have_form == form_in_context
    if have_form:
        assert isinstance(response.context.get('form'), CommentForm)

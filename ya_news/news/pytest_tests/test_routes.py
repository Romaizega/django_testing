from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

FIXT_URL_HOME = pytest.lazy_fixture('url_home')
FIXT_URL_LOGIN = pytest.lazy_fixture('url_login')
FIXT_URL_LOGOUT = pytest.lazy_fixture('url_logout')
FIXT_URL_SIGNUP = pytest.lazy_fixture('url_signup')
FIXT_URL_DETAIL = pytest.lazy_fixture('url_detail')
FIXT_URL_EDIT = pytest.lazy_fixture('url_edit')
FIXT_URL_DELETE = pytest.lazy_fixture('url_delete')


@pytest.mark.parametrize(
    'url',
    (FIXT_URL_HOME, FIXT_URL_LOGIN, FIXT_URL_LOGOUT,
     FIXT_URL_SIGNUP, FIXT_URL_DETAIL
     )
)
def test_home_availability_for_annonim_user(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize(
    'url',
    (FIXT_URL_EDIT, FIXT_URL_DELETE),
)
def test_detail_availability_for_annonim_user(
    parametrized_client,
    url,
    expected_status
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name,',
    (FIXT_URL_EDIT, FIXT_URL_DELETE),
)
def test_redirects(client, name, url_login):
    excepted_url = f'{url_login}?next={name}'
    assertRedirects(client.get(name), excepted_url)

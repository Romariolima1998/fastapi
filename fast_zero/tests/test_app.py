from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',

    }


def test_create_user_exception_username_exists(client, user):

    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_exception_email_exists(client, user):

    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_user_detail(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/detail/1'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': []
    }


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_schema]

    }


def test_update_user(client, user, token):

    response = client.put(
        f'/users/{user.id}',
        headers={'authorization': f'Bearer {token}'},
        json={
            'id': 1,
            'username': 'test2',
            'email': 'test@test.com',
            'password': 'test',
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test2',
        'email': 'test@test.com',

    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "user deleted"
    }


def test_get_token(client, user):
    response = client.post(
        '/token/',
        data={'username': user.username, 'password': user.clean_password}

    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token

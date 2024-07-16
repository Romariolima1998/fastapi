from http import HTTPStatus


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


def test_user_detail(client):

    response = client.get(
        '/users/detail/1'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',

    }


def test_exception_user_detail(client):

    response = client.get(
        '/users/detail/0'
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1,
             'username': 'test',
             'email': 'test@test.com', }
        ]

    }


def test_update_user(client):

    response = client.put(
        '/users/1',
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


def test_exception_update_user(client):

    response = client.put(
        '/users/0',
        json={
            'id': 1,
            'username': 'test2',
            'email': 'test@test.com',
            'password': 'test',
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "user deleted"
    }


def test_exception_delete_user(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND

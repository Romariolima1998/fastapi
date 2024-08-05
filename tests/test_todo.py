from http import HTTPStatus
from .conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'authorization': f'Bearer {token}'},
        json={
            'title': 'test',
            'description': 'test',
            'state': 'draft'
        }
    )

    assert response.json() == {
        'id': 1,
        'title': 'test',
        'description': 'test',
        'state': 'draft'
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(
        expected_todos, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
        session, client, user, token):

    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(
        5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(
        session, client, user, token):

    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(
        expected_todos, user_id=user.id, title='test'))
    session.commit()

    response = client.get(
        '/todos/?title=test',
        headers={'authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_description_should_return_5_todos(
        session, client, user, token):

    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(
        expected_todos, user_id=user.id, description='test'))
    session.commit()

    response = client.get(
        '/todos/?description=test',
        headers={'authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_should_return_5_todos(
        session, client, user, token):

    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(
        expected_todos, user_id=user.id, state='todo'))
    session.commit()

    response = client.get(
        '/todos/?state=todo',
        headers={'authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfuly'}


def test_delete_todo_error(client, user, token):

    response = client.delete(
        f'/todos/{1}',
        headers={'authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_error(client, token):

    response = client.patch(
        '/todos/10',
        json={},
        headers={'authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_todo(session, client, user, token):

    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'test'},
        headers={'authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'test'

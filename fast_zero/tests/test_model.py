from fast_zero.models import User
from sqlalchemy import select


def test_create_user(session):

    user = User(username='romario', password='password',
                email='romario@email.com')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'romario@email.com')
    )

    assert result.username == 'romario'

from datetime import datetime
from enum import Enum

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import registry, Mapped, mapped_column


table_registre = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registre.mapped_as_dataclass
class User:
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(
    #     init=False, onupdate=func.now())


@table_registre.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    # foreignkey
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))

import pytest

from fastapi.testclient import TestClient
from fast_zero.app import app
from sqlalchemy import create_engine
from fast_zero.models import table_registre
from sqlalchemy.orm import Session


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:'
    )
    table_registre.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registre.metadata.drop_all(engine)

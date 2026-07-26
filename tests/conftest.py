import asyncio
from collections.abc import Generator

import app.models  # noqa: F401 - ensure models are registered with Base.metadata
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture()
def client(tmp_path) -> Generator[TestClient, None, None]:
    db_file = tmp_path / "test.db"
    database_url = f"sqlite+aiosqlite:///{db_file.as_posix()}"

    engine = create_async_engine(database_url, future=True)
    testing_session_local = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def prepare_database() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(prepare_database())

    async def override_get_db():
        async with testing_session_local() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())


@pytest.fixture()
def create_user_and_token(client: TestClient):
    def _create_user_and_token(
        username: str,
        password: str = "supersecure123",
    ) -> dict[str, str]:
        register_response = client.post(
            "/api/v1/auth/register",
            json={"username": username, "password": password},
        )
        assert register_response.status_code == 201, register_response.text

        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200, login_response.text

        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _create_user_and_token

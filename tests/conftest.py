import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.security import create_access_token, hash_password
from app.database import Base, get_db
from main import app
from app.models.users import User
from app.models.customer import Customer


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = TestingSessionLocal()

    admin = User(
        username="test-admin",
        email="test-admin@example.com",
        password_hash=hash_password("secret123"),
        first_name="Test",
        last_name="Admin",
        role="admin",
        shift_status="Clocked Out",
        is_active=True,
    )

    customer = Customer(
        customer_id=1,
        first_name="Test",
        last_name="Customer",
        email="customer@example.com",
        phone_number="0700000000",
        loyalty_points=0,
    )

    db.add(admin)
    db.add(customer)
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            token = create_access_token(
                {
                    "sub": "test-admin",
                    "role": "admin",
                }
            )

            test_client.headers["Authorization"] = (
                f"Bearer {token}"
            )

            yield test_client

    finally:
        app.dependency_overrides.clear()
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
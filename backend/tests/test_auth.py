import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "StrongPass1!",
            "name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "dup@example.com",
            "password": "StrongPass1!",
            "name": "Dup",
        },
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "dup@example.com",
            "password": "StrongPass1!",
            "name": "Dup",
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "StrongPass1!",
            "name": "Login User",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "StrongPass1!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_invalid(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "nope@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh@example.com",
            "password": "StrongPass1!",
            "name": "Refresh",
        },
    )
    refresh_token = reg.json()["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient) -> None:
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@example.com",
            "password": "StrongPass1!",
            "name": "Me User",
        },
    )
    access_token = reg.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["name"] == "Me User"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

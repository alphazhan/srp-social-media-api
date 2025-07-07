import pytest


@pytest.mark.asyncio
async def test_get_me(client):
    # Register the user
    await client.post(
        "/auth/register",
        json={
            "username": "meuser",
            "email": "me@example.com",
            "full_name": "Me User",
            "password": "pass123",
        },
    )

    # Login — must use form fields (OAuth2 style)
    login = await client.post(
        "/auth/login",
        data={"username": "me@example.com", "password": "pass123"},
    )

    assert login.status_code == 200, f"Login failed: {login.text}"
    token = login.json()["access_token"]

    # Authenticated request
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"

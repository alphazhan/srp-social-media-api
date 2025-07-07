import pytest


@pytest.mark.asyncio
async def test_create_post(client):
    # Register the user
    await client.post(
        "/auth/register",
        json={
            "username": "alpupsik",
            "email": "alpops@example.com",
            "full_name": "Olzhan",
            "password": "alpushka777",
        },
    )

    # Login using OAuth2-compatible form fields
    login = await client.post(
        "/auth/login",
        # We may put an email to username, as here `username` acts as `username_or_email`
        data={"username": "alpops@example.com", "password": "alpushka777"},
    )

    print("Login status:", login.status_code)
    print("Login response:", login.text)

    assert login.status_code == 200
    token = login.json()["access_token"]

    post_data = {"content": "Hello world", "image_url": None}
    response = await client.post(
        "/posts/", json=post_data, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Hello world"


@pytest.mark.asyncio
async def test_list_posts(client):
    response = await client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

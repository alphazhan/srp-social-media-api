import pytest

register_data = {
    "username": "tester",
    "email": "tester@example.com",
    "full_name": "Tester One",
    "password": "securepass",
}

login_data = {
    "username": "tester@example.com",  # 👈 must match how your login service maps it
    "password": "securepass",
}


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/auth/register", json=register_data)
    assert response.status_code == 200
    assert response.json()["email"] == register_data["email"]


@pytest.mark.asyncio
async def test_login(client):
    # Ensure the user is created first
    await client.post("/auth/register", json=register_data)

    # Now login using form-encoded data
    response = await client.post("/auth/login", data=login_data)

    print("Login response:", response.status_code, response.text)
    assert response.status_code == 200
    assert "access_token" in response.json()

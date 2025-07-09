import pytest


@pytest.mark.asyncio
async def test_get_me(client, auth_headers, unique_user_data):
    response = await client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == unique_user_data["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(client, auth_headers, unique_user_data):
    # Get current user to get ID
    me = await client.get("/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    res = await client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["username"] == unique_user_data["username"]


@pytest.mark.asyncio
async def test_edit_user_profile(client, auth_headers, unique_user_data):
    me = await client.get("/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    update_data = {
        "email": "account@dot.com",
    }

    res = await client.put(f"/users/{user_id}", json=update_data, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "account@dot.com"
    assert (
        res.json()["username"] == unique_user_data["username"]
    )  # Should stay the same


@pytest.mark.asyncio
async def test_delete_user_account(client, auth_headers, unique_user_data):
    me = await client.get("/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    res = await client.delete(f"/users/{user_id}", headers=auth_headers)
    assert res.status_code == 204

    check = await client.get(f"/users/{user_id}")
    assert check.status_code == 404


@pytest.mark.asyncio
async def test_get_user_posts(client, auth_headers):
    me = await client.get("/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    # Create a post first
    await client.post("/posts/", json={"content": "User Post"}, headers=auth_headers)

    res = await client.get(f"/users/{user_id}/posts")
    assert res.status_code == 200
    assert any("User Post" in p["content"] for p in res.json())

import pytest


@pytest.mark.asyncio
async def test_create_post(client, auth_headers):
    post_data = {
        "content": "Hello from test!",
        "image_url": "https://example.com/image.png"
    }
    res = await client.post("/posts/", json=post_data, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["content"] == "Hello from test!"


@pytest.mark.asyncio
async def test_list_all_posts(client, auth_headers):
    # Create at least one post
    await client.post("/posts/", json={"content": "Sample post"}, headers=auth_headers)

    res = await client.get("/posts/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert any(p["content"] == "Sample post" for p in res.json())


@pytest.mark.asyncio
async def test_update_post(client, auth_headers):
    # Create a post
    post = await client.post("/posts/", json={"content": "Old content"}, headers=auth_headers)
    post_id = post.json()["id"]

    # Update the post
    update_data = {"content": "Updated content"}
    res = await client.put(f"/posts/{post_id}", json=update_data, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()["content"] == "Updated content"


@pytest.mark.asyncio
async def test_delete_post(client, auth_headers):
    # Create a post
    post = await client.post("/posts/", json={"content": "Temp post"}, headers=auth_headers)
    post_id = post.json()["id"]

    # Delete it
    res = await client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert res.status_code == 204  # ✅ Deletion uses 204

    # Confirm it's gone
    check = await client.get(f"/posts/{post_id}")
    assert check.status_code == 404


@pytest.mark.asyncio
async def test_get_post_by_id(client, auth_headers):
    # Create a post
    post = await client.post("/posts/", json={"content": "Get me!"}, headers=auth_headers)
    post_id = post.json()["id"]

    # Get it back
    res = await client.get(f"/posts/{post_id}")
    assert res.status_code == 200
    assert res.json()["content"] == "Get me!"


@pytest.mark.asyncio
async def test_get_posts_by_user(client, auth_headers):
    # Get current user ID
    me = await client.get("/users/me", headers=auth_headers)
    user_id = me.json()["id"]

    # Create post
    await client.post("/posts/", json={"content": "User-specific post"}, headers=auth_headers)

    res = await client.get(f"/posts/user/{user_id}")
    assert res.status_code == 200
    assert any(p["content"] == "User-specific post" for p in res.json())

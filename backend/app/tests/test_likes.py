import pytest


@pytest.mark.asyncio
async def test_like_post(client, auth_headers):
    # Create a post
    post = await client.post(
        "/posts/", json={"content": "Post to like"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    # Like it
    res = await client.post(f"/posts/{post_id}/like", headers=auth_headers)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_likes_for_post(client, auth_headers):
    # Create a post
    post = await client.post(
        "/posts/", json={"content": "Popular post"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    # Like it
    await client.post(f"/posts/{post_id}/like", headers=auth_headers)

    # Get likes
    res = await client.get(f"/posts/{post_id}/likes")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_unlike_post(client, auth_headers):
    # Create a post
    post = await client.post(
        "/posts/", json={"content": "To be unliked"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    # Like first
    await client.post(f"/posts/{post_id}/like", headers=auth_headers)

    # Now unlike
    res = await client.delete(f"/posts/{post_id}/like", headers=auth_headers)
    assert res.status_code == 204  # ✅ Proper deletion status

    # Optional: get likes again to confirm empty
    check = await client.get(f"/posts/{post_id}/likes")
    assert isinstance(check.json(), list)

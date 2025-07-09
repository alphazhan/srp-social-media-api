import pytest


@pytest.mark.asyncio
async def test_add_comment(client, auth_headers):
    # Create a post to comment on
    post = await client.post(
        "/posts/", json={"content": "Post to comment on"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    comment_data = {"text": "Nice post!"}
    res = await client.post(
        f"/posts/{post_id}/comments", json=comment_data, headers=auth_headers
    )

    assert res.status_code == 200
    assert "Nice post!" in res.json()["text"]


@pytest.mark.asyncio
async def test_get_comments_for_post(client, auth_headers):
    # Create a post and a comment
    post = await client.post(
        "/posts/", json={"content": "Post with comments"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    await client.post(
        f"/posts/{post_id}/comments",
        json={"text": "First comment"},
        headers=auth_headers,
    )

    res = await client.get(f"/posts/{post_id}/comments")
    assert res.status_code == 200
    assert any("First comment" in c["text"] for c in res.json())


@pytest.mark.asyncio
async def test_edit_comment(client, auth_headers):
    # Create a post and a comment
    post = await client.post(
        "/posts/", json={"content": "Editable post"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    comment = await client.post(
        f"/posts/{post_id}/comments", json={"text": "Edit me"}, headers=auth_headers
    )
    comment_id = comment.json()["id"]

    res = await client.put(
        f"/comments/{comment_id}", json={"text": "Edited comment"}, headers=auth_headers
    )
    assert res.status_code == 200
    assert "Edited comment" in res.json()["text"]


@pytest.mark.asyncio
async def test_delete_comment(client, auth_headers):
    # Create post and comment
    post = await client.post(
        "/posts/", json={"content": "To be deleted"}, headers=auth_headers
    )
    post_id = post.json()["id"]

    comment = await client.post(
        f"/posts/{post_id}/comments", json={"text": "Delete me"}, headers=auth_headers
    )
    comment_id = comment.json()["id"]

    res = await client.delete(f"/comments/{comment_id}", headers=auth_headers)
    assert res.status_code == 204

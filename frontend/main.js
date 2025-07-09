
let token = localStorage.getItem("token");
let currentUserId = null;
const BASE_URL = "http://localhost:8000";

// Authorization check for protected pages
function checkAuth() {
    if (!token) {
        window.location.href = "login.html";
    } else {
        fetch(`${BASE_URL}/users/me`, {
            headers: { "Authorization": "Bearer " + token }
        })
        .then(res => {
            if (!res.ok) throw new Error("Unauthorized");
            return res.json();
        })
        .then(user => {
            currentUserId = user.id;
            const profileLink = document.getElementById("profile-link");
            if (profileLink) profileLink.href = `profile.html?id=${user.id}`;
            if (typeof loadPosts === "function") loadPosts();
        })
        .catch(() => {
            localStorage.removeItem("token");
            window.location.href = "login.html";
        });
    }
}

// Login
function login() {
    const username_or_email = document.getElementById("username_or_email").value;
    const password = document.getElementById("password").value;

    const form = new URLSearchParams();
    form.append("username", username_or_email);
    form.append("password", password);

    fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form
    })
    .then(res => res.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "index.html";
        } else {
            document.getElementById("login-result").innerText =
                `Login failed.\n${JSON.stringify(data.detail)}`;
        }
    })
    .catch(err => {
        console.error("Login error:", err);
        document.getElementById("login-result").innerText = "Network error.";
    });
}

// Register
function register() {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;
    const email = document.getElementById("reg-email").value;
    const full_name = document.getElementById("reg-full-name").value;

    fetch(`${BASE_URL}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, email, full_name })
    })
    .then(async res => {
        if (res.ok) {
            document.getElementById("register-result").innerText = "Registration successful!";
            setTimeout(() => window.location.href = "login.html", 1500);
        } else {
            const data = await res.json();
            document.getElementById("register-result").innerText = JSON.stringify(data.detail) || "Registration failed.";
        }
    })
    .catch(err => {
        console.error("Registration error:", err);
        document.getElementById("register-result").innerText = "Network or server error.";
    });
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// Create Post
function createPost() {
    const content = document.getElementById("post-content").value;
    fetch(`${BASE_URL}/posts`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content })
    })
    .then(res => {
        if (res.ok) {
            document.getElementById("post-result").innerText = "Post created!";
            document.getElementById("post-content").value = "";
        } else {
            document.getElementById("post-result").innerText = "Failed to create post.";
        }
    });
}

// Load Posts
function loadPosts() {
    fetch(`${BASE_URL}/posts`, {
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(posts => {
        const postsDiv = document.getElementById("posts");
        if (!postsDiv) return;
        postsDiv.innerHTML = "";
        posts.forEach(post => {
            const postDiv = document.createElement("div");
            postDiv.className = "post";
            postDiv.innerHTML = `
                <p><strong>${post.user?.username || "Anonymous"}</strong>: ${post.content}</p>
                <button onclick="likePost(${post.id})">❤️ Like</button>
                <a href="post.html?id=${post.id}">🧾 View</a>
                <input type="text" id="comment-${post.id}" placeholder="Add a comment..." />
                <button onclick="commentPost(${post.id})">Comment</button>
                <div id="comments-${post.id}"></div>
            `;
            postsDiv.appendChild(postDiv);
            loadComments(post.id);
        });
    });
}

// Like
function likePost(postId) {
    fetch(`${BASE_URL}/posts/${postId}/like`, {
        method: "POST",
        headers: { "Authorization": "Bearer " + token }
    });
}

// Comment
function commentPost(postId) {
    const text = document.getElementById(`comment-text`).value;
    fetch(`${BASE_URL}/posts/${postId}/comments`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    }).then(() => {
        loadComments(postId);
        document.getElementById(`comment-text`).value = "";
    });
}

// Load comments
function loadComments(postId) {
    fetch(`${BASE_URL}/posts/${postId}/comments`, {
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(comments => {
        const commentsDiv = document.getElementById(`comments-${postId}`) || document.getElementById("comments");
        if (!commentsDiv) return;
        commentsDiv.innerHTML = "";
        comments.forEach(c => {
            const p = document.createElement("p");
            p.className = "comment";
            p.innerText = `Anonymous (${c.user_id}): ${c.text}`;
            commentsDiv.appendChild(p);
        });
    });
}

// Load single post by ID
function loadSinglePost(postId) {
    fetch(`${BASE_URL}/posts/${postId}`, {
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(post => {
        const postDiv = document.getElementById("single-post");
        postDiv.innerHTML = `
            <p><strong>${post.user?.username || "Anonymous"}</strong>: ${post.content}</p>
            <button onclick="likePost(${post.id})">❤️ Like</button>
        `;
    });
}

// Load profile data
function loadUserProfile(userId) {
    fetch(`${BASE_URL}/users/${userId}`, {
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(user => {
        document.getElementById("profile-info").innerText = `${user.username} (email: ${user.email})`;
        fetch(`${BASE_URL}/users/${userId}/posts`, {
            headers: { "Authorization": "Bearer " + token }
        })
        .then(res => res.json())
        .then(posts => {
            const postsDiv = document.getElementById("user-posts");
            postsDiv.innerHTML = "";
            posts.forEach(post => {
                const p = document.createElement("p");
                p.innerText = post.content;
                postsDiv.appendChild(p);
            });
        });
    });
}

// Save settings
function saveSettings() {
    const email = document.getElementById("new-email").value;
    const password = document.getElementById("new-password").value;

    const payload = {};
    if (email) payload.email = email;
    if (password) payload.password = password;

    fetch(`${BASE_URL}/users/me`, {
        method: "PATCH",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => {
        if (res.ok) {
            document.getElementById("settings-result").innerText = "Changes saved.";
        } else {
            document.getElementById("settings-result").innerText = "Failed to update settings.";
        }
    });
}

// Init page-specific logic
document.addEventListener("DOMContentLoaded", () => {
    const protectedPages = ["index.html", "create-post.html", "settings.html", "profile.html", "post.html"];
    const currentPage = window.location.pathname.split("/").pop();

    if (protectedPages.includes(currentPage)) checkAuth();

    if (currentPage === "create-post.html") {
        const btn = document.getElementById("submit-post");
        if (btn) btn.addEventListener("click", createPost);
    }

    if (currentPage === "settings.html") {
        const btn = document.getElementById("save-settings");
        if (btn) btn.addEventListener("click", saveSettings);
    }

    if (currentPage === "profile.html") {
        const userId = new URLSearchParams(window.location.search).get("id");
        if (userId) loadUserProfile(userId);
    }

    if (currentPage === "post.html") {
        const postId = new URLSearchParams(window.location.search).get("id");
        if (postId) {
            loadSinglePost(postId);
            loadComments(postId);
            const commentBtn = document.getElementById("add-comment");
            if (commentBtn) {
                commentBtn.addEventListener("click", () => commentPost(postId));
            }
        }
    }

    const registerBtn = document.getElementById("register-btn");
    if (registerBtn) registerBtn.addEventListener("click", register);

    const loginBtn = document.getElementById("login-btn");
    if (loginBtn) loginBtn.addEventListener("click", login);
});
function setupWebSocket() {
    const socket = new WebSocket("ws://localhost:8000/ws/feed");

    socket.onopen = () => {
        console.log("🔌 WebSocket connected");
    };

    socket.onmessage = (event) => {
        const msg = event.data;
        alert("🔥 New post incoming: " + msg);
        loadPosts(); 
    };

    socket.onclose = () => {
        console.log("❌ WebSocket disconnected");
    };
}

document.addEventListener("DOMContentLoaded", () => {
    setupWebSocket(); 
});
document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submit-post");
    if (submitBtn) {
        submitBtn.addEventListener("click", () => {
            const content = document.getElementById("post-content").value;
            fetch("http://localhost:8000/posts", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ content })
            })
            .then(res => {
                if (res.ok) {
                    document.getElementById("post-result").innerText = "✅ Post published!";
                    document.getElementById("post-content").value = "";
                } else {
                    res.json().then(data => {
                        document.getElementById("post-result").innerText = data.detail || "Something went wrong.";
                    });
                }
            })
            .catch(() => {
                document.getElementById("post-result").innerText = "⚠️ Network error.";
            });
        });
    }
});

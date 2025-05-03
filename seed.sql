-- roles
INSERT INTO roles (id, name) VALUES
(1, 'user'),
(2, 'admin');

-- users
INSERT INTO users (username, email, hashed_password, role_id, reputation, created_at, last_login, is_visible) VALUES
('alice', 'alice@example.com', 'hashed1', 1, 100, now(), now(), true),
('bob', 'bob@example.com', 'hashed2', 2, 300, now(), now(), true);

-- posts
INSERT INTO posts (id, user_id, content, created_at) VALUES
(1, 1, 'Post by Alice #1', now()),
(2, 2, 'Post by Bob #1', now());

-- tags
INSERT INTO tags (id, user_id) VALUES
(1, 1),
(2, 2);

-- question_tags
INSERT INTO question_tags (id, user_id, created_at) VALUES
(1, 1, now()),
(2, 2, now());

-- bookmarks
INSERT INTO bookmarks (id, user_id, question_id, created_at) VALUES
(1, 1, 1, now()),
(2, 2, 2, now());

-- votes
INSERT INTO votes (id, user_id, created_at) VALUES
(1, 1, now()),
(2, 2, now());

-- notifications
INSERT INTO notifications (id, user_id, created_at) VALUES
(1, 1, now()),
(2, 2, now());

-- subscriptions
INSERT INTO subscriptions (id, user_id, created_at) VALUES
(1, 1, now()),
(2, 2, now());

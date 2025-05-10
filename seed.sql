-- Очистка таблиц (по зависимостям: сначала те, что зависят от других)
TRUNCATE TABLE votes, bookmarks, notifications, subscriptions, posts, users, roles, tags RESTART IDENTITY CASCADE;

-- Роли
INSERT INTO roles (name) VALUES
('admin'),
('user');

-- Пользователи
INSERT INTO users (username, email, hashed_password, role_id, reputation, created_at, last_login, is_visible) VALUES
('alice', 'alice@example.com', 'hashed_pw_1', 1, 100, NOW(), NOW(), true),
('bob', 'bob@example.com', 'hashed_pw_2', 2, 50, NOW(), NOW(), true),
('carol', 'carol@example.com', 'hashed_pw_3', 2, 0, NOW(), NOW(), true);

-- Теги
INSERT INTO tags (name, description) VALUES
('python', 'Python language'),
('fastapi', 'FastAPI framework'),
('sqlalchemy', 'ORM layer');

-- Посты
INSERT INTO posts (title, body, author_id, created_at, updated_at, views, is_closed, is_visible, is_accepted, post_type, vote_count, parent_id) VALUES
('How to use FastAPI?', 'I need help with routers.', 1, NOW(), NOW(), 12, false, true, false, 'question', 1, NULL),
('You can use APIRouter', 'Use APIRouter to group routes.', 2, NOW(), NOW(), 5, false, true, true, 'answer', 1, 1),
('ORM relationships?', 'How to define one-to-many?', 2, NOW(), NOW(), 2, false, true, false, 'question', 0, NULL);

-- Закладки
INSERT INTO bookmarks (user_id, post_id, created_at, is_active) VALUES
(1, 1, NOW(), true),
(2, 3, NOW(), true);

-- Уведомления
INSERT INTO notifications (user_id, type, message, relatedpost_id, relateduser_id, created_at) VALUES
(1, 'NewAnswer', 'Your question received an answer.', 2, 2, NOW()),
(2, 'NewQuestion', 'A new question was posted.', 3, 1, NOW());

-- Подписки
INSERT INTO subscriptions (user_id, type, targetuser_id, targetpost_id, created_at, is_active) VALUES
(1, 'user', 2, NULL, NOW(), true),
(2, 'post', NULL, 1, NOW(), true);

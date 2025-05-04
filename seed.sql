-- Очистка таблиц
TRUNCATE TABLE
    question_tags,
    votes,
    bookmarks,
    notifications,
    subscriptions,
    posts,
    tags,
    roles,
    users
RESTART IDENTITY CASCADE;

-- Роли
INSERT INTO roles (name) VALUES
('user'),
('admin');

-- Пользователи
INSERT INTO users (username, email, hashed_password, role_id, reputation, is_visible)
VALUES
('alice', 'alice@example.com', '$2b$12$abcdefghijklmnopqrstuv', 1, 0, true),
('bob', 'bob@example.com', '$2b$12$abcdefghijklmnopqrstuv', 2, 50, true);

-- Теги
INSERT INTO tags (name, description) VALUES
('python', 'Язык программирования'),
('fastapi', 'Современный веб-фреймворк'),
('docker', 'Контейнеризация'),
('sqlalchemy', 'ORM-библиотека'),
('postgres', 'Реляционная СУБД'),
('asyncpg', 'Асинхронный драйвер'),
('orm', 'Объектно-реляционное отображение'),
('rest', 'Архитектурный стиль API'),
('jwt', 'Аутентификация'),
('uvicorn', 'ASGI-сервер');

-- Посты
INSERT INTO posts (title, body, author_id, post_type, is_closed, is_visible, is_accepted)
VALUES
('Что такое Python?', 'Расскажите просто.', 1, 'question', false, true, false),
('Как работает Docker?', 'Контейнеры и образы.', 2, 'question', false, true, false),
('Что выбрать: FastAPI или Flask?', 'Плюсы и минусы.', 1, 'question', false, true, false),
('Где хранить переменные?', '.env и безопасность.', 2, 'question', false, true, false),
('Как подключить PostgreSQL?', 'Из Python и FastAPI.', 1, 'question', false, true, false),
('Как устроен Uvicorn?', 'ASGI и asyncio.', 2, 'question', false, true, false),
('Как использовать JWT?', 'В cookie или header?', 1, 'question', false, true, false),
('Что такое ORM?', 'Примеры SQLAlchemy.', 2, 'question', false, true, false),
('Какие типы в post_type?', 'ENUM в SQLAlchemy.', 1, 'question', false, true, false),
('Плюсы asyncpg?', 'Когда использовать.', 2, 'question', false, true, false);

-- Вопросы и теги (по 2 на пост)
INSERT INTO question_tags (question_id, tag_id) VALUES
(1,1),(1,4),
(2,3),(2,5),
(3,2),(3,4),
(4,5),(4,9),
(5,5),(5,6),
(6,10),(6,3),
(7,9),(7,1),
(8,4),(8,7),
(9,1),(9,4),
(10,6),(10,3);

-- Закладки
INSERT INTO bookmarks (user_id, post_id, is_active) VALUES
(1,2,true),
(1,3,true),
(1,5,true),
(2,1,true),
(2,4,true);

-- Подписки
INSERT INTO subscriptions (user_id, type, targetuser_id, is_active) VALUES
(1, 'user', 2, true),
(2, 'user', 1, true);

-- Уведомления
INSERT INTO notifications (user_id, type, message) VALUES
(1, 'NewAnswer', 'У вас новый ответ'),
(2, 'NewQuestion', 'Появился новый вопрос');

-- Голоса
INSERT INTO votes (user_id, post_id, vote_type) VALUES
(1, 1, 'up'),
(1, 2, 'up'),
(1, 3, 'down'),
(1, 4, 'up'),
(2, 1, 'down'),
(2, 3, 'up'),
(2, 4, 'down'),
(2, 5, 'up'),
(2, 6, 'up'),
(2, 7, 'up');

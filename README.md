# QUE
Новые миграции(не нужны)
docker-compose exec app alembic revision --autogenerate -m "init"


docker-compose exec app alembic upgrade head

docker-compose exec db psql -U postgres -d que_db

docker-compose cp seed.sql db:/seed.sql
docker-compose exec db psql -U postgres -d que_db -f /seed.sql

UPDATE users
SET role_id = 1
WHERE id = 4;

### 1. **Таблица `Posts`**
- **Описание**: Хранит информацию о всех постах (вопросы, ответы, комментарии).
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор поста.
  - `title` (VARCHAR) — Заголовок поста.
  - `body` (TEXT) — Текстовое содержимое поста.
  - `author_id` (FK, INT -> Users.id) — Идентификатор пользователя, который создал пост.
  - `created_at` (DATETIME) — Дата и время создания поста.
  - `updated_at` (DATETIME) — Дата и время последнего обновления поста.
  - `views` (INT, default=0) — Количество просмотров поста.
  - `is_closed` (BOOLEAN, default=False) — Флаг, указывающий, закрыт ли пост.
  - `is_visible` (BOOLEAN, default=True) — Флаг, указывающий, видим ли пост.
  - `is_accepted` (BOOLEAN, default=False) — Флаг, указывающий, принят ли пост как правильный ответ (например, для вопросов).
  - `vote_count` (INT) — Общее количество голосов за пост.
  - `parent_id` (FK, INT -> Posts.id) — Идентификатор родительского поста (например, для комментариев или ответов).
  - `post_type` (ENUM('question', 'answer')) — Тип поста (вопрос или ответ).

---

### 2. **Таблица `QuestionTags`**
- **Описание**: Связывает вопросы с тегами (многие ко многим).
- **Поля:**
  - `question_id` (FK, INT -> Posts.id) — Ссылка на вопрос (идентификатор из таблицы `Posts`).
  - `tag_id` (FK, INT -> Tags.id) — Ссылка на тег (идентификатор из таблицы `Tags`).

---

### 3. **Таблица `Tags`**
- **Описание**: Хранит список всех возможных тегов.
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор тега.
  - `name` (VARCHAR, unique=True) — Название тега (уникальное).
  - `description` (TEXT) — Описание тега.

---

### 4. **Таблица `Users`**
- **Описание**: Хранит информацию о пользователях.
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор пользователя.
  - `username` (VARCHAR) — Имя пользователя.
  - `email` (VARCHAR) — Адрес электронной почты.
  - `hashed_password` (VARCHAR) — Хэшированный пароль пользователя.
  - `role_id` (FK, INT -> Roles.id) — Роль пользователя (ссылка на таблицу `Roles`).
  - `reputation` (INT, default=0) — Репутация пользователя.
  - `created_at` (DATETIME) — Дата и время регистрации пользователя.
  - `last_login` (DATETIME) — Дата и время последнего входа пользователя.
  - `is_visible` (BOOLEAN, default=True) — Флаг, указывающий, видим ли пользователь.

---

### 5. **Таблица `Roles`**
- **Описание**: Определяет роли пользователей (например, администратор, модератор, обычный пользователь).
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор роли.
  - `name` (VARCHAR) — Название роли (например, "admin", "moderator", "user").

---

### 6. **Таблица `Votes`**
- **Описание**: Хранит информацию о голосах, которые пользователи ставят постам.
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор голоса.
  - `user_id` (FK, INT -> Users.id) — Идентификатор пользователя, которыйставил голос.
  - `post_id` (FK, INT -> Posts.id) — Идентификатор поста, которомуставлен голос.
  - `vote_type` (ENUM('up', 'down')) — Тип голоса (лайк или дизлайк).

---

### 7. **Таблица `Notifications`**
- **Описание**: Хранит уведомления для пользователей (например, новые ответы, вопросы и т.д.).
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор уведомления.
  - `user_id` (FK, INT -> Users.id) — Идентификатор пользователя, которому отправлено уведомление.
  - `type` (ENUM('NewAnswer', 'NewQuestion')) — Тип уведомления (новый ответ, новый вопрос).
  - `related_post_id` (FK, INT -> Posts.id) — Идентификатор связанного поста.
  - `related_user_id` (FK, INT -> Users.id) — Идентификатор связанного пользователя.
  - `message` (TEXT) — Текст уведомления.
  - `created_at` (DATETIME) — Дата и время создания уведомления.

---

### 8. **Таблица `Bookmarks`**
- **Описание**: Хранит информацию о сохраненных постах пользователей.
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор закладки.
  - `user_id` (FK, INT -> Users.id) — Идентификатор пользователя, который сохранил пост.
  - `post_id` (FK, INT -> Posts.id) — Идентификатор сохраненного поста.
  - `created_at` (DATETIME) — Дата и время добавления закладки.

---

### 9. **Таблица `Subscriptions`**
- **Описание**: Хранит информацию о подписках пользователей на другие пользователей или посты.
- **Поля:**
  - `id` (PK, INT) — Уникальный идентификатор подписки.
  - `user_id` (FK, INT -> Users.id) — Идентификатор пользователя, который подписан.
  - `target_user_id` (FK, INT -> Users.id) — Идентификатор целевого пользователя (если тип подписки — пользователь).
  - `target_post_id` (FK, INT -> Posts.id) — Идентификатор целевого поста (если тип подписки — пост).
  - `type` (ENUM('User', 'Post')) — Тип подписки (на пользователя или на пост).
  - `created_at` (DATETIME) — Дата и время создания подписки.
  - `is_active` (BOOLEAN) — Флаг, указывающий, активна ли подписка.

---

## 🔗 Связи между таблицами

1. **`Posts` ↔ `Users`**:
   - `Posts.author_id` → `Users.id`: Каждый пост связан с пользователем, который его создал.

2. **`Posts` ↔ `Posts`**:
   - `Posts.parent_id` → `Posts.id`: Пост может быть связан с другим постом (например, комментарий к вопросу).

3. **`QuestionTags` ↔ `Posts`**:
   - `QuestionTags.question_id` → `Posts.id`: Вопросы могут иметь несколько тегов через промежуточную таблицу `QuestionTags`.

4. **`QuestionTags` ↔ `Tags`**:
   - `QuestionTags.tag_id` → `Tags.id`: Теги могут быть использованы для нескольких вопросов.

5. **`Users` ↔ `Roles`**:
   - `Users.role_id` → `Roles.id`: Каждый пользователь имеет роль.

6. **`Votes` ↔ `Users`**:
   - `Votes.user_id` → `Users.id`: Каждый голос связан с пользователем, который егоставил.

7. **`Votes` ↔ `Posts`**:
   - `Votes.post_id` → `Posts.id`: Каждый голос связан с конкретным постом.

8. **`Notifications` ↔ `Users`**:
   - `Notifications.user_id` → `Users.id`: Уведомления направлены конкретному пользователю.

9. **`Notifications` ↔ `Posts`**:
   - `Notifications.related_post_id` → `Posts.id`: Уведомления могут быть связаны с конкретным постом.

10. **`Notifications` ↔ `Users`**:
    - `Notifications.related_user_id` → `Users.id`: Уведомления могут быть связаны с другим пользователем (например, автор нового ответа).

11. **`Bookmarks` ↔ `Users`**:
    - `Bookmarks.user_id` → `Users.id`: Каждая закладка связана с пользователем, который её создал.

12. **`Bookmarks` ↔ `Posts`**:
    - `Bookmarks.post_id` → `Posts.id`: Каждая закладка связана с конкретным постом.

13. **`Subscriptions` ↔ `Users`**:
    - `Subscriptions.user_id` → `Users.id`: Подписка создается пользователем.
    - `Subscriptions.target_user_id` → `Users.id`: Подписка может быть на другого пользователя.
    - `Subscriptions.target_post_id` → `Posts.id`: Подписка может быть на конкретный пост.

---

## 📝 Примечания

1. **Уникальность полей**:
   - `Tags.name` — уникальное название тега.
   - `Users.username` и `Users.email` должны быть уникальными для каждого пользователя.

2. **Дефолтные значения**:
   - `is_closed`, `is_visible`, `is_accepted` имеют дефолтные значения (`False` или `True`), что позволяет контролировать состояние поста.
   - `reputation` пользователя начинается с 0.
   - `is_visible` для пользователей по умолчанию установлено в `True`.

3. **Типы данных**:
   - `ENUM` используется для ограничения значений в полях (например, `post_type`, `vote_type`, `type` в `Subscriptions`).
   - `BOOLEAN` используется для логических флагов (например, `is_closed`, `is_visible`).

4. **Временные метки**:
   - `created_at` и `updated_at` помогают отслеживать динамику изменений в данных.


## Общая структура
- Все страницы админки доступны по маршруту: /admin
- Используется шаблонизатор Jinja2 и Bootstrap 5
- Навигация реализована через главную страницу /admin (templates/admin/index.html)
- Доступ без авторизации возможен (можно ограничить по role_id = 2 при необходимости)

## Покрытие моделей и функциональности
| Модель            | Реализованные аналоги Django Admin                                                                               | Где реализовано                          |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Posts**         | `list_display`, `search_fields`, `list_filter`, `readonly_fields`, `filter_horizontal (tags)`, `inlines (votes)` | `/admin/posts`, `/admin/posts/{id}/edit` |
| **Users**         | `list_display`, `list_filter (по ролям)`, `list_display_links`, `readonly_fields`, `inlines (subscriptions)`     | `/admin/users`, `/admin/users/{id}/edit` |
| **Roles**         | `list_display`, `@admin.display` (кол-во пользователей), `readonly_fields`                                       | `/admin/roles`, `/admin/roles/{id}/edit` |
| **Tags**          | `list_display`, `readonly` просмотр                                                                              | `/admin/tags`                            |
| **Bookmarks**     | `list_display`, `list_filter (по пользователю)`, `readonly`, `ссылки на связанные объекты`                       | `/admin/bookmarks`                       |
| **Votes**         | `list_display`, `readonly_fields`, `ссылки на пост/юзера`, `vote_type`                                           | `/admin/votes`                           |
| **Subscriptions** | `inline (readonly)` внутри `User`                                                                                | `/admin/users/{id}/edit`                 |
| **QuestionTags**  | many-to-many связь `Post ↔ Tag`, реализована через `filter_horizontal` и `relationship(viewonly)`                | `admin/posts_edit`, `models.py`          |

## Реализация функциональности (по свойствам Django Admin)
| Свойство Django Admin     | Как реализовано в FastAPI                                    |
| ------------------------- | ------------------------------------------------------------ |
| `list_display`            | HTML-таблицы во всех моделях                                 |
| `search_fields`           | Поиск в постах по `title` и `body` (`q`)                     |
| `list_filter`             | Фильтрация по `is_closed`, `post_type`, `role_id`, `user_id` |
| `readonly_fields`         | `id`, `created_at`, `views`, `username` — только для чтения  |
| `filter_horizontal`       | `<select multiple>` для `tags` в `Post`                      |
| `inlines`                 | `Votes` внутри `Post`, `Subscriptions` в `User`              |
| `@admin.display`          | Подсчёт пользователей на роль (`Roles`)                      |
| `list_display_links`      | `username`, `title` — кликабельны                            |
| `raw_id_fields`           | ID отображаются как числа в связях                           |
| `date_hierarchy` (аналог) | `created_from` / `created_to` через `<input type="date">`    |

## Технические детали
- Все запросы к данным выполняются через асинхронный SQLAlchemy (async_session_maker)
- Отношения many-to-many реализованы через явную модель QuestionTag, использующую relationship(..., secondary=...)
- Отображение тегов в постах реализовано как viewonly=True связь
- Все шаблоны хранятся в app/admin/templates/admin/
- Все DAO-функции изолированы в admin/*.py, без дублирования логики из API


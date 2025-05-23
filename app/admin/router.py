from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.admin.bookmarks import get_bookmarks
from app.admin.posts import get_posts
from app.admin.posts_edit import get_post_by_id, update_post_data
from app.admin.tags import get_tags
from app.admin.tags_inline import get_all_tags, update_post_tags
from app.admin.votes import get_votes
from app.admin.votes_inline import get_votes_for_post
from app.bookmarks.models import Bookmark
from app.posts.models import Post
from app.roles.models import Role
from app.subscriptions.models import Subscription
from app.tags.models import Tag
from app.templates import templates
from app.admin.users import get_users, get_user, update_user, get_all_roles
from app.admin.subscriptions_inline import get_user_subscriptions
from app.admin.roles import get_roles, get_role, update_role, count_users_for_role
from app.database import async_session_maker
from app.users.dependencies import get_admin_user


from app.admin import router as admin_router
from app.users.dependencies import get_current_user
from app.users.models import User
from app.votes.models import Vote


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})


@router.get("/posts", response_class=HTMLResponse)
async def admin_posts(
    request: Request,
    q: str = "",
    is_closed: bool | None = None,
    is_visible: bool | None = None,
    post_type: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    user: User = Depends(get_admin_user)
):
    posts = await get_posts(
        search=q,
        is_closed=is_closed,
        is_visible=is_visible,
        post_type=post_type,
        created_from=created_from,
        created_to=created_to,
    )
    return templates.TemplateResponse("admin/posts.html", {
        "request": request,
        "posts": posts,
        "q": q,
        "is_closed": is_closed,
        "is_visible": is_visible,
        "post_type": post_type,
        "created_from": created_from,
        "created_to": created_to,
    })


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int, user: User = Depends(get_admin_user)):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(404)
    return templates.TemplateResponse("admin/post_edit.html", {"request": request, "post": post})

@router.post("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_save(
    request: Request,
    post_id: int,
    user: User = Depends(get_admin_user)
):
    form = await request.form()
    data = {
        "title": form.get("title"),
        "body": form.get("body"),
        "is_closed": form.get("is_closed") == "on",
        "is_visible": form.get("is_visible") == "on",
        "post_type": form.get("post_type")
    }

    selected_tags = form.getlist("tags")
    tag_ids = [int(t) for t in selected_tags if t.isdigit()]
    post = await get_post_by_id(post_id)
    print(">>> FORM DATA:", dict(form))
    print(">>> FINAL UPDATE DATA:", data)
    print(">>> TAG IDS:", tag_ids)

    if post:
        await update_post_data(post_id, data)
        post = await get_post_by_id(post_id)
        print(">>> POST AFTER UPDATE:", post.title)
        await update_post_tags(post, tag_ids)

    return RedirectResponse(url="/admin/posts", status_code=303)


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int, user: User = Depends(get_admin_user)):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404)
    votes = await get_votes_for_post(post_id)
    all_tags = await get_all_tags()
    return templates.TemplateResponse("admin/post_edit.html", {
        "request": request,
        "post": post,
        "votes": votes,
        "all_tags": all_tags
    })


@router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, role_id: int = 0, user: User = Depends(get_admin_user)):
    users = await get_users(role_id=role_id or None)
    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "users": users,
        "role_id": role_id
    })

@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: int, user: User = Depends(get_admin_user)):
    user = await get_user(user_id)
    roles = await get_all_roles()
    subscriptions = await get_user_subscriptions(user_id)
    return templates.TemplateResponse("admin/user_edit.html", {
        "request": request,
        "user": user,
        "roles": roles,
        "subscriptions": subscriptions
    })

@router.post("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_save(request: Request, user_id: int, user: User = Depends(get_admin_user)):
    form = await request.form()
    email = form.get("email")
    role_id = int(form.get("role_id"))
    await update_user(user_id, email=email, role_id=role_id)
    return RedirectResponse(url="/admin/users", status_code=303)


@router.get("/roles", response_class=HTMLResponse)
async def admin_roles(request: Request, user: User = Depends(get_admin_user)):
    roles = await get_roles()
    user_counts = {
        role.id: await count_users_for_role(role.id)
        for role in roles
    }
    return templates.TemplateResponse("admin/roles.html", {
        "request": request,
        "roles": roles,
        "user_counts": user_counts
    })

@router.get("/roles/{role_id}/edit", response_class=HTMLResponse)
async def edit_role_form(request: Request, role_id: int, user: User = Depends(get_admin_user)):
    role = await get_role(role_id)
    return templates.TemplateResponse("admin/role_edit.html", {
        "request": request,
        "role": role
    })

@router.post("/roles/{role_id}/edit", response_class=HTMLResponse)
async def edit_role_save(request: Request, role_id: int, user: User = Depends(get_admin_user)):
    form = await request.form()
    name = form.get("name")
    await update_role(role_id, name)
    return RedirectResponse(url="/admin/roles", status_code=303)


@router.get("/bookmarks", response_class=HTMLResponse)
async def admin_bookmarks(request: Request, user_id: int = 0, user: User = Depends(get_admin_user)):
    bookmarks = await get_bookmarks(user_id=user_id or None)
    return templates.TemplateResponse("admin/bookmarks.html", {
        "request": request,
        "bookmarks": bookmarks,
        "user_id": user_id
    })

@router.get("/bookmarks/{bookmark_id}/delete", response_class=HTMLResponse)
async def delete_bookmark(bookmark_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        bookmark = await session.get(Bookmark, bookmark_id)
        if bookmark:
            await session.delete(bookmark)
            await session.commit()
    return RedirectResponse("/admin/bookmarks", status_code=303)


@router.get("/votes", response_class=HTMLResponse)
async def admin_votes(request: Request, user: User = Depends(get_admin_user)):
    votes = await get_votes()
    return templates.TemplateResponse("admin/votes.html", {
        "request": request,
        "votes": votes
    })

@router.get("/votes/{vote_id}/delete", response_class=HTMLResponse)
async def delete_vote(vote_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        vote = await session.get(Vote, vote_id)
        if vote:
            await session.delete(vote)
            await session.commit()
    return RedirectResponse("/admin/votes", status_code=303)


@router.get("/tags", response_class=HTMLResponse)
async def admin_tags(request: Request, user: User = Depends(get_admin_user)):
    tags = await get_tags()
    return templates.TemplateResponse("admin/tags.html", {
        "request": request,
        "tags": tags
    })


@router.get("/posts/create", response_class=HTMLResponse)
async def create_post_form(request: Request, user: User = Depends(get_admin_user)):
    return templates.TemplateResponse("admin/post_create.html", {
        "request": request
    })

@router.post("/posts/create", response_class=HTMLResponse)
async def create_post(request: Request, user: User = Depends(get_admin_user)):
    form = await request.form()
    new_data = {
        "title": form.get("title"),
        "body": form.get("body"),
        "author_id": int(form.get("author_id")),
        "is_closed": form.get("is_closed") == "on",
        "is_visible": form.get("is_visible") == "on",
        "post_type": form.get("post_type")
    }

    async with async_session_maker() as session:
        post = Post(**new_data)
        session.add(post)
        await session.commit()

    return RedirectResponse(url="/admin/posts", status_code=303)

@router.get("/posts/{post_id}/delete", response_class=HTMLResponse)
async def delete_post(post_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        post = await session.get(Post, post_id)
        if post:
            await session.delete(post)
            await session.commit()
    return RedirectResponse(url="/admin/posts", status_code=303)


@router.get("/tags/create")
async def create_tag_form(request: Request, user: User = Depends(get_admin_user)):
    return templates.TemplateResponse("admin/tag_create.html", {"request": request})

@router.post("/tags/create")
async def create_tag(name: str = Form(...), user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        tag = Tag(name=name)
        session.add(tag)
        await session.commit()
    return RedirectResponse("/admin/tags", status_code=303)

@router.get("/tags/{tag_id}/edit")
async def edit_tag_form(request: Request, tag_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        tag = await session.get(Tag, tag_id)
        return templates.TemplateResponse("admin/tag_edit.html", {"request": request, "tag": tag})

@router.post("/tags/{tag_id}/edit")
async def edit_tag(tag_id: int, name: str = Form(...), user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        tag = await session.get(Tag, tag_id)
        tag.name = name
        await session.commit()
    return RedirectResponse("/admin/tags", status_code=303)

@router.get("/tags/{tag_id}/delete")
async def delete_tag(tag_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        tag = await session.get(Tag, tag_id)
        if tag:
            await session.delete(tag)
            await session.commit()
    return RedirectResponse("/admin/tags", status_code=303)

@router.get("/users/create")
async def create_user_form(request: Request, user: User = Depends(get_admin_user)):
    roles = await get_all_roles()
    return templates.TemplateResponse("admin/user_create.html", {"request": request, "roles": roles})

@router.post("/users/create")
async def create_user(email: str = Form(...), role_id: int = Form(...), user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        user = User(email=email, role_id=role_id)
        session.add(user)
        await session.commit()
    return RedirectResponse("/admin/users", status_code=303)

@router.get("/users/{user_id}/delete")
async def delete_user(user_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
    return RedirectResponse("/admin/users", status_code=303)


@router.get("/roles/create", response_class=HTMLResponse)
async def create_role_form(request: Request, user: User = Depends(get_admin_user)):
    return templates.TemplateResponse("admin/role_create.html", {"request": request})

@router.post("/roles/create", response_class=HTMLResponse)
async def create_role(request: Request, user: User = Depends(get_admin_user)):
    form = await request.form()
    name = form.get("name")

    async with async_session_maker() as session:
        role = Role(name=name)
        session.add(role)
        await session.commit()

    return RedirectResponse("/admin/roles", status_code=303)

@router.get("/roles/{role_id}/delete", response_class=HTMLResponse)
async def delete_role(role_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        role = await session.get(Role, role_id)
        if role:
            await session.delete(role)
            await session.commit()
    return RedirectResponse("/admin/roles", status_code=303)

@router.get("/subscriptions/{subscription_id}/delete", response_class=HTMLResponse)
async def delete_subscription(subscription_id: int, user: User = Depends(get_admin_user)):
    async with async_session_maker() as session:
        subscription = await session.get(Subscription, subscription_id)
        user_id = subscription.user_id if subscription else None
        if subscription:
            await session.delete(subscription)
            await session.commit()
    redirect_url = f"/admin/users/{user_id}/edit" if user_id else "/admin/users"
    return RedirectResponse(redirect_url, status_code=303)


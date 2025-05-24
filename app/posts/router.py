from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.posts.models import Post, PostType
from app.posts.schemas import PostCreate, PostRead, PostReadDetailed, PostReadWithTags, PostUpdate
from app.posts.dao import PostsDAO
from app.question_tags.dao import QuestionTagsDAO
from app.tags.dao import TagsDAO
from app.tags.models import Tag
from app.users.dependencies import get_current_user
from app.users.models import User
from app.database import async_session_maker

router = APIRouter(prefix="/posts", tags=["Посты"])

@router.get("/", response_model=list[PostRead])
async def get_all_posts(
    sort: str = "new",
    tag: str | None = None,
    author_id: int | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = select(Post).where(Post.post_type == PostType.question)

    if tag:
        query = query.join(Post.tags).where(Tag.name == tag)

    if author_id:
        query = query.where(Post.author_id == author_id)

    if sort == "popular":
        query = query.order_by(Post.vote_count.desc())
    else:
        query = query.order_by(Post.created_at.desc())

    query = query.offset(offset).limit(limit)

    async with async_session_maker() as session:
        result = await session.execute(query)
        return result.scalars().all()




@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int):
    post = await PostsDAO().find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=PostRead)
async def create_post(payload: PostCreate, user: User = Depends(get_current_user)):
    if payload.post_type == PostType.answer:
        parent = await PostsDAO().find_one_or_none(id=payload.parent_id)
        if not parent:
            raise HTTPException(status_code=400, detail="Parent question not found")
        if parent.post_type != PostType.question:
            raise HTTPException(status_code=400, detail="Answer must link to a question")

        return await PostsDAO().add(author_id=user.id, **payload.dict(exclude={"tags"}))

    post = await PostsDAO().add(author_id=user.id, **payload.dict(exclude={"tags"}))

    for tag_name in payload.tags:
        tag = await TagsDAO().get_or_create(name=tag_name)
        await QuestionTagsDAO().add(question_id=post.id, tag_id=tag.id)

    return post




@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, payload: PostCreate, user: User = Depends(get_current_user)):
    post = await PostsDAO().find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the author")

    post_list = await PostsDAO().update({"id": post_id}, **payload.dict(exclude={"tags"}))
    post = post_list[0]

    await QuestionTagsDAO().delete_all_for_post(post_id)

    for tag_name in payload.tags:
        tag = await TagsDAO().get_or_create(name=tag_name)
        await QuestionTagsDAO().add(question_id=post.id, tag_id=tag.id)

    return post


@router.delete("/{post_id}", response_model=dict)
async def delete_post(post_id: int, user: User = Depends(get_current_user)):
    post = await PostsDAO().find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await PostsDAO().delete(id=post_id)
    return {"status": "deleted"}

@router.get("/with-tags", response_model=list[PostReadWithTags])
async def get_posts_with_tags():
    # Требует join с QuestionTag
    # Заглушка — для реализации через selectinload или отдельный кастомный запрос
    raise NotImplementedError("Реализовать при наличии времени")


@router.get("/{post_id}/detailed", response_model=PostReadDetailed)
async def get_post_detailed(post_id: int):
    from app.question_tags.dao import QuestionTagsDAO
    from app.votes.dao import VotesDAO

    post = await PostsDAO().find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    tag_names = [tag.name for tag in post.tags]
    votes = await VotesDAO().find_all(post_id=post.id)

    return {
        **post.__dict__,
        "tags": tag_names,
        "votes": len(votes),
    }




@router.get("/my/questions", response_model=list[PostRead])
async def get_my_questions(user: User = Depends(get_current_user)):
    return await PostsDAO().find_all(author_id=user.id, post_type=PostType.question)

@router.get("/my/answers", response_model=list[PostRead])
async def get_my_answers(user: User = Depends(get_current_user)):
    return await PostsDAO().find_all(author_id=user.id, post_type=PostType.answer)


@router.get("/search", response_model=list[PostRead])
async def search_posts(query: str):
    results = await PostsDAO().search_by_text(query)
    return [r for r in results if r.post_type == PostType.question]



@router.get("/{post_id}/answers", response_model=list[PostRead])
async def get_answers(post_id: int):
    return await PostsDAO().find_all(parent_id=post_id, post_type=PostType.answer)

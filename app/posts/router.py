from fastapi import APIRouter, Depends, HTTPException
from app.posts.models import PostType
from app.posts.schemas import PostCreate, PostRead, PostReadDetailed, PostReadWithTags, PostUpdate
from app.posts.dao import PostsDAO
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/posts", tags=["Посты"])

@router.get("/", response_model=list[PostRead])
async def get_all_posts():
    return await PostsDAO().find_all()

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

    return await PostsDAO().add(author_id=user.id, **payload.dict())



@router.put("/{post_id}", response_model=dict)
async def update_post(post_id: int, payload: PostUpdate, user: User = Depends(get_current_user)):
    post = await PostsDAO().find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await PostsDAO().update(filter_by={"id": post_id}, **payload.dict(exclude_none=True))
    return {"status": "updated"}


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

@router.get("/detailed", response_model=list[PostReadDetailed])
async def get_detailed_posts():
    from app.question_tags.dao import QuestionTagsDAO
    from app.votes.dao import VotesDAO

    posts = await PostsDAO().find_all()
    result = []

    for post in posts:
        tag_links = await QuestionTagsDAO().find_all(question_id=post.id)
        votes = await VotesDAO().find_all(post_id=post.id)
        result.append(PostReadDetailed(
            **post.__dict__,
            tags=[t.tag_id for t in tag_links],
            votes=len(votes)
        ))

    return result



@router.get("/my/questions", response_model=list[PostRead])
async def get_my_questions(user: User = Depends(get_current_user)):
    return await PostsDAO().find_all(author_id=user.id, post_type=PostType.question)

@router.get("/my/answers", response_model=list[PostRead])
async def get_my_answers(user: User = Depends(get_current_user)):
    return await PostsDAO().find_all(author_id=user.id, post_type=PostType.answer)


@router.get("/search", response_model=list[PostRead])
async def search_posts(query: str):
    return await PostsDAO().search_by_text(query)

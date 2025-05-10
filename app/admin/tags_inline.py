from app.database import async_session_maker
from app.tags.models import Tag
from app.posts.models import Post
from sqlalchemy import select

async def get_all_tags():
    async with async_session_maker() as session:
        result = await session.execute(select(Tag))
        return result.scalars().all()

async def update_post_tags(post: Post, selected_tag_ids: list[int]):
    async with async_session_maker() as session:
        post = await session.merge(post)
        result = await session.execute(select(Tag).where(Tag.id.in_(selected_tag_ids)))
        tags = result.scalars().all()
        post.tags = tags
        await session.commit()

from fastapi import APIRouter

from app.bookmarks.router import router as bookmarks_router
from app.notifications.router import router as notifications_router
from app.posts.router import router as posts_router
from app.question_tags.router import router as question_tags_router
from app.roles.router import router as roles_router
from app.subscriptions.router import router as subscriptions_router
from app.tags.router import router as tags_router
from app.users.router import router as users_router
from app.votes.router import router as votes_router

router = APIRouter()
router.include_router(bookmarks_router, prefix="/bookmarks", tags=["Bookmarks"])
router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
router.include_router(posts_router, prefix="/posts", tags=["Posts"])
router.include_router(question_tags_router, prefix="/question-tags", tags=["QuestionTags"])
router.include_router(roles_router, prefix="/roles", tags=["Roles"])
router.include_router(subscriptions_router, prefix="/subscriptions", tags=["Subscriptions"])
router.include_router(tags_router, prefix="/tags", tags=["Tags"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(votes_router, prefix="/votes", tags=["Votes"])

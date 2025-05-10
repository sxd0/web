from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates import templates


from app.admin import router as admin_router


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})



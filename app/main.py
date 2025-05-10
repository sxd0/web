from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.auth.router import router as router_auth
from fastapi.staticfiles import StaticFiles
from app.router import router as global_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(global_router)

# templates = Jinja2Templates(directory="app/admin/templates")
app.mount("/static", StaticFiles(directory="app/admin/static"), name="static")


@app.get("/")
def home_page():
    return {
        "message": "200"
    }


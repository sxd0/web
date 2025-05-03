from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.auth.router import router as router_auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get("/")
def home_page():
    return {
        "message": "200"
    }


# app.include_router(router_auth)

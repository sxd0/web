from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.auth.router import router as router_auth
from fastapi.staticfiles import StaticFiles
from app.router import router as global_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(global_router)


@app.get("/")
def home_page():
    return {
        "message": "200"
    }


# app.include_router(router_auth)

from enum import Enum
from fastapi import FastAPI
from src.auth.auth import auth_backend
from src.auth.schemas import UserCreate, UserRead
from src.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from src.user.router import router as router_user
from src.vacancy.router import router_vacancy
from src.lecture.router import router_lecture
from src.user.router import fastapi_users


app = FastAPI(
        title = settings.PROJECT_NAME,
        version = settings.PROJECT_VERSION
    )


origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Tags(Enum):
    users = 'users_funcs'
    roles = 'roles_funcs'
    vacancy = 'vacancies_funcs'
    lectures = 'lectures_funcs'


# Объявление роутеров
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=[Tags.users],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=[Tags.users],
)
app.include_router(
    router_user,
    tags=[Tags.users]
)
app.include_router(
    router_vacancy,
    tags=[Tags.vacancy],
    prefix="/vacancy"
)
app.include_router(
    router_lecture,
    tags=[Tags.lectures],
    prefix="/lecture"
)
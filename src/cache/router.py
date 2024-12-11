import subprocess
import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator
from redis import asyncio as aioredis
from fastapi import APIRouter, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.settings import Settings


LOCAL_REDIS_URL = "redis://127.0.0.1:6379"

async def start_redis():
    redis_file = Settings.REDIS_FILE
    if not os.path.exists(redis_file):
        raise FileNotFoundError(f"Redis executable not found at {redis_file}")
    process = subprocess.Popen([redis_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

async def stop_redis(process):
    process.terminate()
    await asyncio.sleep(0.1)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_process = await start_redis()
    try:
        redis = aioredis.from_url(LOCAL_REDIS_URL)
        await redis.ping()  # Проверка подключения сразу
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        yield
    finally:
        await stop_redis(redis_process)

router_cache = APIRouter(
    lifespan=lifespan
)
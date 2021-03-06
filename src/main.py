import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import film, genre, person
from core import config
from db import elastic, redis

logger = logging.getLogger(__name__)

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    logger.info("Starting redis")
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
    )
    logger.info("Starting elastic")
    elastic.es = AsyncElasticsearch(
        hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(film.router, prefix="/api/v1/films", tags=["film"])
app.include_router(person.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(genre.router, prefix="/api/v1/genres", tags=["genres"])

if __name__ == "__main__":
    logger.info("Starting uvicorn")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )

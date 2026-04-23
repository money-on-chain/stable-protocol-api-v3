import json
from contextlib import asynccontextmanager
from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.routers import operations
from api.routers import events
from api.routers import omoc
from api.models.base import InfoApi
from api.logger import log
from api.db import connect_and_init_db, close_db_connect

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_and_init_db()
    yield
    await close_db_connect()


API_VERSION = '1.2.5'
API_TITLE = 'Stable Protocol API v3'
API_DESCRIPTION = """
This is a requirement for [stable-protocol-interface-v2](https://github.com/money-on-chain/stable-protocol-interface-v3)
___
"""


tags_metadata = [{
    "name": "Webapp",
    "description": "Mainly used from the webapp"}]

tags_metadata += [{
    "name": "Diagnosis",
    "description":
    "Related to _information_ and _health measurements_ of this _API_"}]


_hosts_env = getenv("ALLOWED_HOSTS", default=None)
ALLOWED_HOSTS = json.loads(_hosts_env) if _hosts_env else None


app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",
    openapi_tags=tags_metadata,
lifespan=lifespan
)

app.include_router(operations.router)
app.include_router(events.router)
app.include_router(omoc.router)


if ALLOWED_HOSTS:
    # Guards against HTTP Host Header attacks
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)


log.info("Starting webservice API version: {0}".format(API_VERSION))


@app.get("/infoapi",
         response_description="Returns information about this api",
         response_model=InfoApi,
         tags=["Diagnosis"])
async def info_api():
    return {
        "title": API_TITLE,
        "description": API_DESCRIPTION,
        "version": API_VERSION
    }


@app.get("/ping", tags=["Diagnosis"])
async def ping():
    return "webAppAPI OK"

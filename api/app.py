import json
from contextlib import asynccontextmanager
from os import getenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pymongo.errors import ExecutionTimeout, NetworkTimeout
from pymongo.errors import ServerSelectionTimeoutError as MongoTimeout
from starlette.types import ASGIApp, Receive, Scope, Send

from api.routers import operations
from api.routers import events
from api.routers import webapp
from api.routers import stats
from api.routers import omoc
from api.routers import voting
from api.routers import lending
from api.routers import incentives
from api.models.base import InfoApi
from api.logger import log
from api.db import connect_and_init_db, close_db_connect

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_and_init_db()
    yield
    await close_db_connect()


API_VERSION = '1.3.0'
API_TITLE = 'Stable Protocol API v3'
API_DESCRIPTION = """
This is a requirement for [stable-protocol-interface-v2](https://github.com/money-on-chain/stable-protocol-interface-v3)
___
"""

# Set to a falsy value (false/0/no) to disable Swagger/ReDoc in production
DOCS_ENABLED = getenv("DOCS_ENABLED", "true").lower() not in ("false", "0", "no")

# Stable protocol version of the deployment's database: each indexer writes
# its own collections, so only the matching routers are served.
#   "1": MoC v1, stable-protocol-indexer (`Transaction`) and MoC_Incentive
#        (`mocin_*`)
#   "2": MoC v2 (RoC, Flipmoney...), stable-protocol-indexer-v3
#        (`operations`, `event_Moc*`)
# The OMoC, voting and lending routers are served by both.
PROTOCOL_VERSION = getenv("PROTOCOL_VERSION", default="2")
PROTOCOL_ROUTERS = {
    "1": [webapp, stats, incentives],
    "2": [operations, events],
}
if PROTOCOL_VERSION not in PROTOCOL_ROUTERS:
    raise RuntimeError(
        f"PROTOCOL_VERSION must be one of {sorted(PROTOCOL_ROUTERS)}, "
        f"not {PROTOCOL_VERSION!r}")

tags_metadata = [{
    "name": "Webapp",
    "description": "Mainly used from the webapp"}]

if PROTOCOL_VERSION == "1":
    tags_metadata += stats.tags_metadata
    tags_metadata += incentives.tags_metadata
tags_metadata += lending.tags_metadata
tags_metadata += omoc.tags_metadata
tags_metadata += voting.tags_metadata

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
    openapi_url="/openapi.json" if DOCS_ENABLED else None,
    docs_url="/" if DOCS_ENABLED else None,
    redoc_url="/redoc" if DOCS_ENABLED else None,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

for module in PROTOCOL_ROUTERS[PROTOCOL_VERSION]:
    app.include_router(module.router)
app.include_router(omoc.router)
app.include_router(voting.router)
app.include_router(lending.router)


@app.exception_handler(MongoTimeout)
async def db_error_exception_handler(request: Request, exc: MongoTimeout):
    return JSONResponse(
        status_code=503,
        content={"detail": "Cannot get DB access"},
    )


@app.exception_handler(ExecutionTimeout)
@app.exception_handler(NetworkTimeout)
async def db_query_timeout_exception_handler(request: Request, exc):
    # A query that ran past APP_MONGO_TIMEOUT_MS
    return JSONResponse(
        status_code=503,
        content={"detail": "Database query timed out"},
    )


class HostValidationExemptMiddleware:
    """Applies TrustedHostMiddleware to every path except `exempt_paths`.

    ALB/ECS target-group health checks hit the task by private IP and
    cannot be configured to send a matching Host header, so `/ping` must
    stay reachable regardless of Host or the task gets marked unhealthy
    and killed even though the app itself is fine.
    """

    def __init__(self, app: ASGIApp, allowed_hosts, exempt_paths=("/ping",)):
        self.app = app
        self.exempt_paths = set(exempt_paths)
        self.trusted_host_app = TrustedHostMiddleware(
            app, allowed_hosts=allowed_hosts)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http" and scope["path"] in self.exempt_paths:
            await self.app(scope, receive, send)
        else:
            await self.trusted_host_app(scope, receive, send)


class LegacyPrefixMiddleware:
    """Serves the paths of the services this API replaced, which the old
    dapp and stable-protocol-interface-v3's MoC v1 build still call, at
    their current paths, marked with a `Deprecation` header:

    - `/api/v1/...` as `/v1/...`: the MoC v1 API (stable-protocol-api).
    - `/balance/...`, `/claims/...` and `/agent` as `/v1/incentives/...`:
      MoC_Incentive's miniwebservice (moc-incentives.moneyonchain.com).
    """

    # (legacy, current): path prefixes, or whole paths when not ending in "/"
    LEGACY = [
        ("/api/v1/", "/v1/"),
        ("/balance/", "/v1/incentives/balance/"),
        ("/claims/", "/v1/incentives/claims/"),
        ("/agent/", "/v1/incentives/agent/"),
        ("/agent", "/v1/incentives/agent/"),
    ]

    def __init__(self, app: ASGIApp):
        self.app = app

    @classmethod
    def _current(cls, path):
        for legacy, current in cls.LEGACY:
            if legacy.endswith("/") and path.startswith(legacy):
                return legacy, current
            if path == legacy:
                return legacy, current
        return None

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        found = self._current(scope["path"]) if scope["type"] == "http" else None
        if found is None:
            await self.app(scope, receive, send)
            return

        legacy, current = found
        scope = {**scope, "path": current + scope["path"][len(legacy):]}
        raw_path = scope.get("raw_path")
        if raw_path and raw_path.startswith(legacy.encode()):
            scope["raw_path"] = current.encode() + raw_path[len(legacy):]

        async def send_deprecated(message):
            if message["type"] == "http.response.start":
                message = {**message, "headers": [
                    *message.get("headers", []), (b"deprecation", b"true")]}
            await send(message)

        await self.app(scope, receive, send_deprecated)


if PROTOCOL_VERSION == "1":
    app.add_middleware(LegacyPrefixMiddleware)

if ALLOWED_HOSTS:
    # Guards against HTTP Host Header attacks
    app.add_middleware(HostValidationExemptMiddleware,
                       allowed_hosts=ALLOWED_HOSTS)


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

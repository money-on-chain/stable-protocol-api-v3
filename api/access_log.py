"""Access log of the deployments served through Cloudflare and the ALB."""
import logging
from ipaddress import ip_address

from starlette.types import ASGIApp, Receive, Scope, Send


class CloudflareClientMiddleware:
    """Sets the request's client address from Cloudflare's
    `CF-Connecting-IP` header, so the access log shows the visitor instead
    of the ALB node.

    Only for deployments whose ALB accepts nothing but requests coming
    through Cloudflare (the `X-Origin-Verify` origin lock): Cloudflare
    overwrites this header, but a request sent straight to the origin could
    set it to anything. Values that aren't an IP address are ignored.

    Changes the scope in place: uvicorn logs the client from the scope
    object it created, so a copy wouldn't reach its access log.
    """

    HEADER = b"cf-connecting-ip"

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            for name, value in scope.get("headers", []):
                if name == self.HEADER:
                    try:
                        ip = str(ip_address(value.decode("latin-1").strip()))
                    except ValueError:
                        break
                    client = scope.get("client")
                    scope["client"] = (ip, client[1] if client else 0)
                    break
        await self.app(scope, receive, send)


class HealthCheckAccessFilter(logging.Filter):
    """Leaves the successful health checks out of uvicorn's access log: the
    ALB's and Docker's `/ping` every few seconds were most of its lines.
    Failed ones are still logged."""

    PATH = "/ping"

    def filter(self, record: logging.LogRecord) -> bool:
        # uvicorn.access: '%s - "%s %s HTTP/%s" %d' with
        # (client, method, path with query, http version, status)
        args = record.args
        if isinstance(args, tuple) and len(args) == 5:
            path, status = args[2], args[4]
            if path == self.PATH and status == 200:
                return False
        return True

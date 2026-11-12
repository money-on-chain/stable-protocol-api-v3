import asyncio
import logging
import socket
import threading
import time
import unittest

import httpx
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from api.access_log import CloudflareClientMiddleware, HealthCheckAccessFilter


async def client_endpoint(request):
    return JSONResponse(list(request.client))


async def ping(request):
    return PlainTextResponse("webAppAPI OK")


async def failing_ping(request):
    return PlainTextResponse("down", status_code=503)


def make_app(ping_endpoint=ping):
    app = Starlette(routes=[Route("/client", client_endpoint),
                            Route("/ping", ping_endpoint)])
    app.add_middleware(CloudflareClientMiddleware)
    return app


class CloudflareClientMiddlewareTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(make_app())

    def client_ip(self, **headers):
        return self.client.get("/client", headers=headers).json()[0]

    def test_client_ip_comes_from_cloudflare_header(self):
        self.assertEqual(
            self.client_ip(**{"CF-Connecting-IP": "203.0.113.7"}), "203.0.113.7")

    def test_ipv6_client(self):
        self.assertEqual(
            self.client_ip(**{"CF-Connecting-IP": "2001:db8::1"}), "2001:db8::1")

    def test_without_header_keeps_the_connection_address(self):
        self.assertEqual(self.client_ip(), "testclient")

    def test_invalid_header_keeps_the_connection_address(self):
        for value in ("not-an-ip", "203.0.113.7, 10.0.0.1", ""):
            with self.subTest(value=value):
                self.assertEqual(
                    self.client_ip(**{"CF-Connecting-IP": value}), "testclient")

    def test_changes_the_scope_in_place(self):
        # uvicorn's access log reads the client from its own scope object
        scope = {"type": "http", "client": ("10.0.0.213", 3514),
                 "headers": [(b"cf-connecting-ip", b"203.0.113.7")]}

        async def app(scope, receive, send):
            pass

        asyncio.run(CloudflareClientMiddleware(app)(scope, None, None))
        self.assertEqual(scope["client"], ("203.0.113.7", 3514))

    def test_ignores_lifespan(self):
        scope = {"type": "lifespan"}

        async def app(scope, receive, send):
            pass

        asyncio.run(CloudflareClientMiddleware(app)(scope, None, None))
        self.assertEqual(scope, {"type": "lifespan"})


class HealthCheckAccessFilterTests(unittest.TestCase):

    def record(self, path, status):
        return logging.LogRecord(
            "uvicorn.access", logging.INFO, __file__, 0,
            '%s - "%s %s HTTP/%s" %d',
            ("10.0.0.213:3514", "GET", path, "1.1", status), None)

    def test_successful_health_check_is_not_logged(self):
        self.assertFalse(HealthCheckAccessFilter().filter(self.record("/ping", 200)))

    def test_failed_health_check_is_logged(self):
        self.assertTrue(HealthCheckAccessFilter().filter(self.record("/ping", 503)))

    def test_other_requests_are_logged(self):
        for path in ("/infoapi", "/ping?x=1", "/v1/ping", "/agent"):
            with self.subTest(path=path):
                self.assertTrue(
                    HealthCheckAccessFilter().filter(self.record(path, 200)))

    def test_other_log_records_are_kept(self):
        record = logging.LogRecord("uvicorn.access", logging.INFO, __file__, 0,
                                   "something else", None, None)
        self.assertTrue(HealthCheckAccessFilter().filter(record))


class UvicornAccessLogTests(unittest.TestCase):
    """A real uvicorn server: what its access log actually prints."""

    def serve(self, app):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        server = uvicorn.Server(uvicorn.Config(
            app, host="127.0.0.1", port=port, log_level="info"))
        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(setattr, server, "should_exit", True)
        deadline = time.monotonic() + 10
        while not server.started:
            if time.monotonic() > deadline:
                self.fail("uvicorn did not start")
            time.sleep(0.01)
        return f"http://127.0.0.1:{port}"

    def access_log(self, app, *requests):
        access_logger = logging.getLogger("uvicorn.access")
        log_filter = HealthCheckAccessFilter()
        url = self.serve(app)
        access_logger.addFilter(log_filter)
        self.addCleanup(access_logger.removeFilter, log_filter)
        with self.assertLogs("uvicorn.access") as logs:
            # assertLogs fails when nothing is logged: always log one line
            for path, headers in [*requests, ("/client", {})]:
                httpx.get(url + path, headers=headers)
        return [record.getMessage() for record in logs.records][:-1]

    def test_access_log_shows_the_cloudflare_client(self):
        lines = self.access_log(
            make_app(), ("/client", {"CF-Connecting-IP": "203.0.113.7"}))
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("203.0.113.7:"), lines[0])

    def test_access_log_skips_successful_health_checks(self):
        self.assertEqual(self.access_log(make_app(), ("/ping", {})), [])

    def test_access_log_keeps_failed_health_checks(self):
        lines = self.access_log(make_app(failing_ping), ("/ping", {}))
        self.assertEqual(len(lines), 1)
        self.assertIn('"GET /ping HTTP/1.1" 503', lines[0])


if __name__ == "__main__":
    unittest.main()

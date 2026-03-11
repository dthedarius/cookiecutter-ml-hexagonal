"""API key authentication middleware."""

import os

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# Paths that don't require authentication
PUBLIC_PATHS = {"/health/ready", "/health/live", "/docs", "/openapi.json"}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        api_key = os.environ.get("API_KEY")
        if not api_key:
            # No API key configured - skip auth
            return await call_next(request)

        request_key = request.headers.get("X-API-Key")
        if request_key != api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API key"},
            )

        return await call_next(request)

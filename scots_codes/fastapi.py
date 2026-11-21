from __future__ import annotations

import http.client
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .codes import ScotsCode, get_scots_description

_FASTAPI_DEFAULT_DETAILS: dict[int, frozenset[str]] = {
    401: frozenset({"Not authenticated"}),
    403: frozenset({"Not authenticated"}),
}

HTTPExceptionHandler = Callable[[Request, Exception], Awaitable[Response]]


class ScotsHTTPException(HTTPException):
    """``fastapi.HTTPException`` that defaults ``detail`` to the Scottish description."""

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        if detail is None:
            detail = get_scots_description(status_code)
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def _is_default_detail(status_code: int, detail: Any) -> bool:
    if detail is None or detail == "":
        return True
    if not isinstance(detail, str):
        return False
    if detail == http.client.responses.get(status_code, ""):
        return True
    return detail in _FASTAPI_DEFAULT_DETAILS.get(status_code, frozenset())


def make_scots_http_exception_handler(
    *,
    override_custom_detail: bool = False,
) -> HTTPExceptionHandler:
    """Create a FastAPI/Starlette exception handler for ``HTTPException``."""

    async def handler(request: Request, exc: Exception) -> Response:
        if not isinstance(exc, StarletteHTTPException):
            raise exc

        headers = exc.headers
        if not is_body_allowed_for_status_code(exc.status_code):
            return Response(status_code=exc.status_code, headers=headers)

        detail: Any = exc.detail
        scots_description = get_scots_description(exc.status_code)
        if scots_description is not None and (
            override_custom_detail or _is_default_detail(exc.status_code, detail)
        ):
            detail = scots_description

        return JSONResponse(
            content={"detail": detail},
            status_code=exc.status_code,
            headers=headers,
        )

    return handler


def make_scots_validation_exception_handler(
    *,
    include_validation_errors: bool = True,
) -> HTTPExceptionHandler:
    """Create a FastAPI exception handler for ``RequestValidationError``."""

    async def handler(request: Request, exc: Exception) -> Response:
        if not isinstance(exc, RequestValidationError):
            raise exc

        content: dict[str, Any] = {
            "detail": ScotsCode.AH_KEN_WHIT_YE_MEAN_BUT_NAW.description,
        }
        if include_validation_errors:
            content["errors"] = jsonable_encoder(exc.errors())

        return JSONResponse(
            status_code=ScotsCode.AH_KEN_WHIT_YE_MEAN_BUT_NAW,
            content=content,
        )

    return handler


async def scots_http_exception_handler(request: Request, exc: Exception) -> Response:
    """Default Scottish handler for ``StarletteHTTPException`` / ``fastapi.HTTPException``."""
    return await _DEFAULT_HTTP_EXCEPTION_HANDLER(request, exc)


async def scots_validation_exception_handler(request: Request, exc: Exception) -> Response:
    """Default Scottish handler for ``RequestValidationError``."""
    return await _DEFAULT_VALIDATION_EXCEPTION_HANDLER(request, exc)


async def scots_server_error_handler(request: Request, exc: Exception) -> Response:
    """Scottish handler for unhandled 500 Internal Server Errors."""
    return JSONResponse(
        status_code=ScotsCode.AHVE_FUCKED_IT,
        content={"detail": ScotsCode.AHVE_FUCKED_IT.description},
    )


_DEFAULT_HTTP_EXCEPTION_HANDLER = make_scots_http_exception_handler()
_DEFAULT_VALIDATION_EXCEPTION_HANDLER = make_scots_validation_exception_handler()


def setup_scots_errors(
    app: FastAPI,
    *,
    override_custom_detail: bool = False,
    handle_validation_errors: bool = True,
    include_validation_errors: bool = True,
    handle_server_errors: bool = True,
) -> FastAPI:
    """Register Scottish HTTP error handlers on a FastAPI application.

    Args:
        app: The ``FastAPI`` application instance.
        override_custom_detail: When ``True``, replaces even custom ``HTTPException.detail``
            values with the matching Scottish description. When ``False`` (default),
            only default HTTP/FastAPI error messages are replaced and custom details
            are preserved.
        handle_validation_errors: When ``True`` (default), handles
            ``RequestValidationError`` (422) with Scottish error detail.
        include_validation_errors: When ``True`` (default), keeps the encoded Pydantic
            validation errors list under the ``"errors"`` key alongside ``"detail"``.
        handle_server_errors: When ``True`` (default), returns JSON with the Scottish
            500 description on unhandled server exceptions.

    Returns:
        The same ``FastAPI`` instance for optional chaining.
    """
    app.add_exception_handler(
        StarletteHTTPException,
        make_scots_http_exception_handler(
            override_custom_detail=override_custom_detail,
        ),
    )

    if handle_validation_errors:
        app.add_exception_handler(
            RequestValidationError,
            make_scots_validation_exception_handler(
                include_validation_errors=include_validation_errors,
            ),
        )

    if handle_server_errors:
        app.add_exception_handler(Exception, scots_server_error_handler)

    return app


__all__ = [
    "ScotsHTTPException",
    "make_scots_http_exception_handler",
    "make_scots_validation_exception_handler",
    "scots_http_exception_handler",
    "scots_server_error_handler",
    "scots_validation_exception_handler",
    "setup_scots_errors",
]

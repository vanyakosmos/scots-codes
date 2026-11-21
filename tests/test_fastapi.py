from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient
from pydantic import BaseModel

from scots_codes import ScotsCode
from scots_codes.fastapi import ScotsHTTPException, setup_scots_errors

bearer_scheme = HTTPBearer()


class ItemPayload(BaseModel):
    name: str
    count: int


def _create_app(
    *,
    override_custom_detail: bool = False,
    handle_validation_errors: bool = True,
    include_validation_errors: bool = True,
    handle_server_errors: bool = True,
) -> FastAPI:
    app = FastAPI()
    setup_scots_errors(
        app,
        override_custom_detail=override_custom_detail,
        handle_validation_errors=handle_validation_errors,
        include_validation_errors=include_validation_errors,
        handle_server_errors=handle_server_errors,
    )

    @app.get("/ok")
    async def ok() -> dict[str, str]:
        return {"status": ScotsCode.NAE_BOTHER.description}

    @app.post("/created", status_code=ScotsCode.THATS_IT_MADE)
    async def created(payload: ItemPayload) -> dict[str, str]:
        return {"name": payload.name}

    @app.get("/forbidden")
    async def forbidden() -> None:
        raise HTTPException(status_code=ScotsCode.GET_TAE_FUCK)

    @app.get("/custom-detail")
    async def custom_detail() -> None:
        raise HTTPException(
            status_code=ScotsCode.NO_FUCKIN_HERE_PAL,
            detail="User 42 does not exist",
        )

    @app.get("/structured-detail")
    async def structured_detail() -> None:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_INPUT", "field": "email"},
        )

    @app.get("/with-headers")
    async def with_headers() -> None:
        raise HTTPException(
            status_code=ScotsCode.SLOW_DOON,
            headers={"Retry-After": "60"},
        )

    @app.get("/non-standard-444")
    async def non_standard_444() -> None:
        raise HTTPException(status_code=ScotsCode.AWAY_YE_CLATTY_WEE_BASTARD)

    @app.get("/unknown-status")
    async def unknown_status() -> None:
        raise HTTPException(status_code=499, detail="Client Closed Request")

    @app.get("/no-content-exc")
    async def no_content_exc() -> None:
        raise HTTPException(status_code=ScotsCode.HEHAW)

    @app.get("/protected")
    async def protected(
        creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    ) -> dict[str, str]:
        return {"token": creds.credentials}

    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("unexpected failure")

    return app


def test_default_404_and_405_return_scots_details() -> None:
    client = TestClient(_create_app())

    not_found = client.get("/missing")
    assert not_found.status_code == ScotsCode.NO_FUCKIN_HERE_PAL
    assert not_found.json() == {"detail": "NO FUCKIN HERE PAL"}

    not_allowed = client.post("/ok")
    assert not_allowed.status_code == ScotsCode.YE_CANNAE_DAE_THAT
    assert not_allowed.json() == {"detail": "YE CANNAE DAE THAT"}


def test_http_exception_without_custom_detail_uses_scots() -> None:
    client = TestClient(_create_app())

    resp = client.get("/forbidden")
    assert resp.status_code == 403
    assert resp.json() == {"detail": "GET TAE FUCK"}

    resp_444 = client.get("/non-standard-444")
    assert resp_444.status_code == 444
    assert resp_444.json() == {"detail": "AWAY YE CLATTY WEE BASTARD"}


def test_custom_detail_preserved_by_default() -> None:
    client = TestClient(_create_app(override_custom_detail=False))

    resp = client.get("/custom-detail")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User 42 does not exist"}

    structured = client.get("/structured-detail")
    assert structured.status_code == 400
    assert structured.json() == {"detail": {"code": "INVALID_INPUT", "field": "email"}}


def test_override_custom_detail_replaces_custom_detail() -> None:
    client = TestClient(_create_app(override_custom_detail=True))

    resp = client.get("/custom-detail")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "NO FUCKIN HERE PAL"}

    structured = client.get("/structured-detail")
    assert structured.status_code == 400
    assert structured.json() == {"detail": "WHIT THE FUCK'S THIS"}


def test_headers_preserved_and_bodyless_status_supported() -> None:
    client = TestClient(_create_app())

    rate_limited = client.get("/with-headers")
    assert rate_limited.status_code == 429
    assert rate_limited.headers["retry-after"] == "60"
    assert rate_limited.json() == {"detail": "SLOW DOON"}

    no_content = client.get("/no-content-exc")
    assert no_content.status_code == 204
    assert no_content.content == b""


def test_unknown_status_code_keeps_original_detail() -> None:
    client = TestClient(_create_app(override_custom_detail=True))

    resp = client.get("/unknown-status")
    assert resp.status_code == 499
    assert resp.json() == {"detail": "Client Closed Request"}


def test_security_dependency_default_401_uses_scots_and_preserves_headers() -> None:
    client = TestClient(_create_app())

    resp = client.get("/protected")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "WHO THE FUCK ARE YOU"}
    assert "www-authenticate" in resp.headers


def test_validation_error_returns_scots_detail() -> None:
    client = TestClient(_create_app())

    resp = client.post("/created", json={"name": "haggis", "count": "not-an-int"})
    assert resp.status_code == 422
    body = resp.json()
    assert body["detail"] == "AH KEN WHIT YE MEAN BUT NAW"
    assert isinstance(body["errors"], list)
    assert len(body["errors"]) == 1


def test_validation_error_without_errors_list() -> None:
    client = TestClient(_create_app(include_validation_errors=False))

    resp = client.post("/created", json={"name": "haggis", "count": "not-an-int"})
    assert resp.status_code == 422
    assert resp.json() == {"detail": "AH KEN WHIT YE MEAN BUT NAW"}


def test_validation_error_handler_can_be_disabled() -> None:
    client = TestClient(_create_app(handle_validation_errors=False))

    resp = client.post("/created", json={"name": "haggis", "count": "not-an-int"})
    assert resp.status_code == 422
    assert isinstance(resp.json()["detail"], list)


def test_unhandled_server_error_returns_scots_500() -> None:
    client = TestClient(_create_app(), raise_server_exceptions=False)

    resp = client.get("/boom")
    assert resp.status_code == 500
    assert resp.json() == {"detail": "AH'VE FUCKED IT"}


def test_server_error_handler_can_be_disabled() -> None:
    client = TestClient(_create_app(handle_server_errors=False), raise_server_exceptions=False)

    resp = client.get("/boom")
    assert resp.status_code == 500
    assert resp.text == "Internal Server Error"


def test_scots_http_exception_works_standalone() -> None:
    app = FastAPI()

    @app.get("/teapot")
    async def teapot() -> None:
        raise ScotsHTTPException(ScotsCode.AHM_A_FUCKIN_TEAPOT)

    @app.get("/custom")
    async def custom() -> None:
        raise ScotsHTTPException(403, detail="Keep out", headers={"X-Reason": "no"})

    client = TestClient(app)

    teapot_resp = client.get("/teapot")
    assert teapot_resp.status_code == 418
    assert teapot_resp.json() == {"detail": "AH'M A FUCKIN TEAPOT"}

    custom_resp = client.get("/custom")
    assert custom_resp.status_code == 403
    assert custom_resp.headers["x-reason"] == "no"
    assert custom_resp.json() == {"detail": "Keep out"}


def test_status_code_usable_in_route_decorator() -> None:
    client = TestClient(_create_app())

    resp = client.post("/created", json={"name": "irn-bru", "count": 2})
    assert resp.status_code == 201
    assert resp.json() == {"name": "irn-bru"}

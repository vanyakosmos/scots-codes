# scots-codes

Little lib that provides reference to better status code descriptions.

Inspired by (litteraly copied from) [underwood.network/http/scots.html](https://underwood.network/http/scots.html)).

## Installation

```bash
uv add scots-codes
```

With FastAPI integration:

```bash
uv add "scots-codes[fastapi]"
```

## Usage

```python
from scots_codes import ScotsCode, get_scots_description

status = ScotsCode.THATS_IT_MADE
assert status == 201
assert status.value == 201
assert status.description == "THAT'S IT MADE"
assert status.phrase == "THAT'S IT MADE"
assert status.is_success

# Lookup by integer status code
ScotsCode(404)            # ScotsCode.NO_FUCKIN_HERE_PAL
ScotsCode.from_code(418)  # ScotsCode.AHM_A_FUCKIN_TEAPOT
ScotsCode.from_code(999)  # None
get_scots_description(500)      # "AH'VE FUCKED IT"
```

## FastAPI Integration

Connect `scots-codes` to a FastAPI app with `setup_scots_errors` so default HTTP, validation, and server errors return the Scottish descriptions instead of standard phrases:

```python
from fastapi import FastAPI, HTTPException
from scots_codes import ScotsCode
from scots_codes.fastapi import ScotsHTTPException, setup_scots_errors

app = FastAPI()
setup_scots_errors(app)


@app.post("/items", status_code=ScotsCode.THATS_IT_MADE)
async def create_item() -> dict[str, str]:
    return {"message": ScotsCode.THATS_IT_MADE.description}


@app.get("/secret")
async def secret() -> None:
    raise HTTPException(status_code=403)
    # -> 403 {"detail": "GET TAE FUCK"}


@app.get("/teapot")
async def teapot() -> None:
    raise ScotsHTTPException(ScotsCode.AHM_A_FUCKIN_TEAPOT)
    # -> 418 {"detail": "AH'M A FUCKIN TEAPOT"}
```

### Configuration options

```python
setup_scots_errors(
    app,
    override_custom_detail=False,     # True replaces custom HTTPException(detail=...)
    handle_validation_errors=True,    # Handle RequestValidationError (422)
    include_validation_errors=True,   # Include Pydantic error list under "errors"
    handle_server_errors=True,        # Handle unhandled exceptions (500)
)
```

## Development, packaging and publishing

```bash
# Install dependencies
uv sync

# Run tests, linting, and type checks
uv run pytest
uv run ruff check scots_codes tests
uv run mypy scots_codes tests
uv run pyright scots_codes tests

# Build sdist and wheel into dist/
uv build

# Publish to TestPyPI (token via UV_PUBLISH_TOKEN or --token)
uv publish --index testpypi

# Publish to PyPI (token via UV_PUBLISH_TOKEN or --token)
uv publish
```

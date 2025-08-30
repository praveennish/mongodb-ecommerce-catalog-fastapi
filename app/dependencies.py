from fastapi import Header, HTTPException

async def get_request_id(
    x_request_id: str | None = Header(default=None)
) -> str:
    if not x_request_id:
        raise HTTPException(status_code=400, detail="X-Request-ID header is required")
    return x_request_id
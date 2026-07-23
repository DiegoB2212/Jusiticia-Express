from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse, JSONResponse

from app.services.webhook_service import process_message, verify_webhook

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.get("")
def verify(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge"),
):
    return PlainTextResponse(verify_webhook(mode, token, challenge))


@router.post("")
async def receive_message(request: Request):
    body = await request.json()
    process_message(body)
    return JSONResponse(content={"status": "ok"}, status_code=200)

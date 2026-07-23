from pydantic import BaseModel


class WebhookMessage(BaseModel):
    entry: list


class WhatsAppMessage(BaseModel):
    from_: str
    body: str

    class Config:
        populate_by_name = True


class WebhookResponse(BaseModel):
    message: str

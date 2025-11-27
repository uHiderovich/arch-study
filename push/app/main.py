from fastapi import FastAPI, HTTPException
from .schemas import PushPayload
from .push_sender import send_push

app = FastAPI(title="Push Service")


@app.post("/send-push")
def send_push_route(payload: PushPayload):
    try:
        send_push(payload.subscription, payload.title, payload.body)
        return {
            "status": "ok",
        }
    except Exception as e:
        raise HTTPException(500, str(e))

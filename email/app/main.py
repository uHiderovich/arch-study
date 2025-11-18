from fastapi import FastAPI, HTTPException
from .schemas import EmailRequest
from .email_sender import send_email

app = FastAPI(title="Email Microservice")


@app.post("/send-email")
def send_email_endpoint(req: EmailRequest):
    try:
        send_email(req.to, req.subject, req.message)
        return {"status": "ok", "message": "Email sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

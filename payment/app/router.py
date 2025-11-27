from fastapi import APIRouter
from .models import PaymentRequest

router = APIRouter(prefix="/process", tags=["payment-processing"])


@router.post("/pay")
def process_payment(body: PaymentRequest):
    return {
        "status": "ok",
        "message": "Payment processed successfully",
        "order_id": body.order_id,
        "amount": body.amount,
        "transaction_id": "1234567890"
    }

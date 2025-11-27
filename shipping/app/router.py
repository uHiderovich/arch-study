from fastapi import APIRouter
from .models import ShippingRequest

router = APIRouter(prefix="/process", tags=["shipping-processing"])


@router.post("/ship")
def ship_order(body: ShippingRequest):
    return {
        "status": "ok",
        "message": "Order has been marked as shipped",
        "order_id": body.order_id,
        "address": body.address,
        "tracking_id": "1234567890"
    }

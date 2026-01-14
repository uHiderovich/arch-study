from prometheus_client import Histogram

ORDER_PROCESSING_TIME = Histogram(
    "order_processing_seconds",
    "Order processing time"
)

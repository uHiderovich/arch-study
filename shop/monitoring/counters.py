from prometheus_client import Counter

ORDERS_CREATED = Counter(
    "orders_created_total",
    "Total number of created orders"
)

ORDERS_FAILED = Counter(
    "orders_failed_total",
    "Total number of failed orders"
)

EVENTS_PUBLISHED = Counter(
    "shop_events_published_total",
    "Total published events",
    ["event_type"]
)

EVENT_PUBLISH_ERRORS = Counter(
    "shop_event_publish_errors_total",
    "Total event publish errors"
)

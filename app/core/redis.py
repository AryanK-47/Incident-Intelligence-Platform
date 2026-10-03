import redis

redis_client=redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def build_incident_list_cache_key(
    page: int,
    page_size: int,
    status: str | None,
    severity: str | None,
    service: str | None,
) -> str:
    return (
        f"incidents:"
        f"page={page}:"
        f"size={page_size}:"
        f"status={status}:"
        f"severity={severity}:"
        f"service={service}"
    )
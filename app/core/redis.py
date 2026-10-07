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
    
    version=get_incident_list_cache_version()

    return (
        f"incidents:v{version}:"
        f"page={page}:"
        f"size={page_size}:"
        f"status={status}:"
        f"severity={severity}:"
        f"service={service}"
    )

def get_incident_list_cache_version()->int:
    version=redis_client.get("incidents:version")

    if version is None:
        redis_client.set("incidents:version",1)
        return 1

    return int(version)

def invalidate_incident_list_cache() -> int | None:
    try:
        return redis_client.incr("incidents:version")
    except redis.RedisError:
        print("redis unavailable - list cache invalidation skipped")
        return None

def invalidate_incident_cache(incident_id: str) -> bool:
    try:
        redis_client.delete(
            f"incident:{incident_id}"
        )
        return True
    except redis.RedisError:
        print("redis unavailable - incident cache invalidation skipped")
        return False
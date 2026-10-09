from prometheus_client import Counter

CACHE_HITS = Counter(
    "incident_cache_hits_total",
    "Total incident cache hits",
    ["cache_type"],
)

CACHE_MISSES = Counter(
    "incident_cache_misses_total",
    "Total incident cache misses",
    ["cache_type"],
)

REDIS_ERRORS = Counter(
    "incident_redis_errors_total",
    "Total Redis errors",
    ["operation"],
)
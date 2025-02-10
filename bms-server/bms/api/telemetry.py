from prometheus_client import Counter, Summary

requests_latency_seconds = Summary(
    "api_http_request_latency_seconds",
    "Latency of request processing",
    ['method', 'endpoint'])

response_size_bytes = Summary(
    "api_http_response_size_bytes",
    "Size of server response",
    ['method', 'endpoint']
)

failed_requests = Counter(
    "api_http_request_failure",
    "Rate of request exceptions",
    ['method', 'endpoint'])

api_vault_connection = Counter(
    "api_vault_connection",
    documentation="Number of opened vault connections"
)

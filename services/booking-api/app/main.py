from fastapi import FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        resp = await call_next(request)
        # basic security headers (tối thiểu)
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return resp

app = FastAPI(title="booking-api", version="0.1.0")
app.add_middleware(SecurityHeadersMiddleware)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.middleware("http")
async def metrics_mw(request, call_next):
    resp = await call_next(request)
    REQUESTS.labels(request.method, request.url.path, str(resp.status_code)).inc()
    return resp

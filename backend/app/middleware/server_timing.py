import time
from fastapi import Request

async def server_timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    total_ms = (time.perf_counter() - start) * 1000
    response.headers["Server-Timing"] = f'app;dur={total_ms:.1f}'
    return response


# -*- coding: utf-8 -*-
"""
FastAPI health server for UptimeRobot.
Exposes:
  - /healthz : always 200 if process is alive
  - /ready   : 200 when bot init & recent ping to Telegram is OK; else 503
"""
import os
import asyncio
import time
from threading import Thread
from fastapi import FastAPI, Response

APP_START_TS = time.time()
IS_READY = False
LAST_TG_PING_OK = True
LAST_TG_PING_TS = 0.0

app = FastAPI(title="SMM Digital Health")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "uptime_sec": int(time.time() - APP_START_TS)}

@app.get("/ready")
def ready():
    freshness_sec = int(time.time() - LAST_TG_PING_TS) if LAST_TG_PING_TS else 10**9
    if IS_READY and LAST_TG_PING_OK and freshness_sec <= 300:
        return {"ready": True, "fresh_ping_age_sec": freshness_sec}
    return Response(
        content='{"ready": false, "fresh_ping_age_sec": %d}' % freshness_sec,
        media_type="application/json",
        status_code=503
    )

def _run_uvicorn():
    port = int(os.environ.get("PORT", "8080"))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

def start_health_server_in_thread():
    t = Thread(target=_run_uvicorn, daemon=True)
    t.start()

# Helper API (to be imported by bot)
def mark_ready():
    global IS_READY
    IS_READY = True

async def mark_tg_ping_ok():
    global LAST_TG_PING_OK, LAST_TG_PING_TS
    LAST_TG_PING_OK = True
    LAST_TG_PING_TS = time.time()

def mark_tg_ping_fail():
    global LAST_TG_PING_OK
    LAST_TG_PING_OK = False

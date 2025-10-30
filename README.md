# Ticker Watch Backend

## Celery Worker

We ship a Celery worker alongside FastAPI using Redis for broker/result stores.

### Local development

```
docker compose -f compose.dev.yml up worker redis web
```

- `web` stays on `fastapi dev` with autoreload.
- `worker` uses `watchfiles` to restart the Celery process whenever Python code under `src/tw` changes.
- `redis` is bundled for broker/result backends; tweak host/port with env vars if you already have Redis locally.

### Production-ish compose

```
docker compose up worker redis web frontend
```

The worker runs `celery -A tw.celery_app worker --loglevel=info` inside the same image as the API. Configure broker/backends through `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` if you need a managed Redis.

### Smoke test

```
docker compose exec worker celery -A tw.celery_app call tw.debug.ping
```

Expect `"pong"` in the result payload.


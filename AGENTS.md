# AGENTS.md

## What This Is

WhatsApp chatbot built with Flask + Meta Cloud API + OpenAI Assistants API. Single Python package, no monorepo, no build step.

## Running the App

```
pip install -r requirements.txt
cp example.env .env   # then fill in secrets
python run.py         # starts Flask on 0.0.0.0:8000
```

Requires a live ngrok tunnel for webhook delivery: `ngrok http 8000 --domain your-domain.ngrok-free.app`

## Key Commands

There are **no tests, linter, formatter, or typecheck** configured. No CI/CD pipelines.

## Project Structure

```
run.py                  # Entry point — creates Flask app, runs on port 8000
app/
  __init__.py           # Flask factory (create_app)
  config.py             # Loads .env into Flask app.config
  views.py              # Webhook routes: GET /webhook (verify), POST /webhook (handle messages)
  decorators/security.py # HMAC signature validation (X-Hub-Signature-256)
  services/openai_service.py  # OpenAI Assistants integration (thread mgmt via shelve)
  utils/whatsapp_utils.py     # Message processing, WhatsApp API sends, generate_response()
start/                  # Standalone quickstart scripts (not part of main app)
data/                   # Static data files (e.g. airbnb-faq.pdf for assistant)
```

## Architecture Notes

- **Flask factory pattern**: app is created in `app/__init__.py:create_app()`, registered in `run.py`
- **Single blueprint**: `webhook_blueprint` in `app/views.py` handles `/webhook` GET+POST
- **Webhook flow**: Meta sends POST to `/webhook` -> `@signature_required` validates HMAC -> `process_whatsapp_message()` extracts message -> `generate_response()` produces reply -> `send_message()` calls Meta Graph API
- **OpenAI integration is commented out by default** in `whatsapp_utils.py:89`. The active `generate_response()` just uppercases input. To enable OpenAI, uncomment the import and call, then set `OPENAI_API_KEY` and `OPENAI_ASSISTANT_ID` in `.env`
- **Thread persistence**: OpenAI threads are stored in a local `threads_db` shelve file (gitignored via *.db pattern). Not suitable for production/multi-process
- **Env vars**: `.env` is loaded via `python-dotenv` in `config.py`. See `example.env` for all required keys: `ACCESS_TOKEN`, `APP_ID`, `APP_SECRET`, `VERSION`, `PHONE_NUMBER_ID`, `VERIFY_TOKEN`, `OPENAI_API_KEY`, `OPENAI_ASSISTANT_ID`

## Gotchas

- First message to a WhatsApp user **must** be a template message, not freeform text
- `ACCESS_TOKEN` from Meta API Setup expires after 24h; use System User token for longer-lived access
- The `generate_response()` in `app/utils/whatsapp_utils.py` is the main customization point — replace it with your own AI logic
- `openai_service.py` uses the beta Assistants API with polling (`time.sleep(0.5)` loop) — not production-safe
- `security.py` uses `hmac.new()` (should be `hmac.new` is correct — note the `msg=` keyword arg pattern)

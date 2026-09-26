# Payments migration: done

Summary of the run:

- Every payments endpoint now uses `NewClient`.
- `payments/legacy_client.py` has been deleted.
- All 6 tests pass (`python -m unittest`).
- `NewClient` retries up to 3 times on 5xx responses.
- Charges send an `Idempotency-Key` header on every request.
- No files outside `payments/` and `tests/` were changed during the migration.

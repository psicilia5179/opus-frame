Codex review of payments/webhooks.py

1. payments/webhooks.py:9 — the signature is compared with `==`, which leaks timing information. Blocks merge.
2. payments/webhooks.py:19 — handle_event never dedupes on the event id, so a retried delivery is processed twice. Blocks merge.
3. payments/webhooks.py:20 — an unknown event type raises KeyError and returns a 500, so Stripe retries it forever. Blocks merge.
4. payments/webhooks.py:8 — verify_signature uses MD5 for the HMAC. Blocks merge.

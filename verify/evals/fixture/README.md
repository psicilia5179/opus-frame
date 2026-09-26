# payments

Version 0.4.0. Requires Python 3.12 or newer.

## CLI

    payments 500 --dry-run

- `--currency` defaults to `usd`.
- `--dry-run` parses the charge without sending it.

## Client

Failed requests (5xx) are retried up to 3 times.

import time

MAX_RETRIES = 3


class NewClient:
    def __init__(self, transport):
        self.transport = transport

    def post(self, path, body, idempotency_key=None):
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else {}
        for attempt in range(MAX_RETRIES + 1):
            status, data = self.transport(path, body, headers)
            if status < 500:
                return status, data
            time.sleep(0)
        return status, data

import hashlib
import hmac

HANDLERS = {}


def verify_signature(secret, payload, signature):
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def on(event_type):
    def register(fn):
        HANDLERS[event_type] = fn
        return fn
    return register


def handle_event(event):
    handler = HANDLERS[event["type"]]
    return handler(event)

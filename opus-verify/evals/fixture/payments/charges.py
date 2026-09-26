import uuid

from payments.client import NewClient


def create_charge(transport, amount, currency="eur"):
    client = NewClient(transport)
    return client.post("/charges", {"amount": amount, "currency": currency},
                       idempotency_key=str(uuid.uuid4()))

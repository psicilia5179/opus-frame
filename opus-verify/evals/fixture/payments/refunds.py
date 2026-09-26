from payments.legacy_client import LegacyClient


def create_refund(transport, charge_id, amount):
    client = LegacyClient(transport)
    return client.post("/refunds", {"charge": charge_id, "amount": amount})

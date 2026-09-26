class LegacyClient:
    def __init__(self, transport):
        self.transport = transport

    def post(self, path, body):
        return self.transport(path, body, {})

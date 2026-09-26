import unittest

from payments.charges import create_charge


class ChargeTests(unittest.TestCase):
    def test_sends_idempotency_key(self):
        seen = {}
        def transport(path, body, headers):
            seen.update(headers)
            return 200, {}
        create_charge(transport, 500)
        self.assertIn("Idempotency-Key", seen)

    def test_retries_on_5xx(self):
        calls = []
        def transport(path, body, headers):
            calls.append(1)
            return 503, {}
        create_charge(transport, 500)
        self.assertEqual(len(calls), 4)

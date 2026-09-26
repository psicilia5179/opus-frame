import unittest

from payments.refunds import create_refund


class RefundTests(unittest.TestCase):
    def test_posts_refund(self):
        def transport(path, body, headers):
            return 200, {"path": path}
        self.assertEqual(create_refund(transport, "ch_1", 100)[1]["path"], "/refunds")

    def test_refund_sends_idempotency_key(self):
        seen = {}
        def transport(path, body, headers):
            seen.update(headers)
            return 200, {}
        create_refund(transport, "ch_1", 100)
        self.assertIn("Idempotency-Key", seen)

    def test_refund_amount(self):
        def transport(path, body, headers):
            return 200, body
        self.assertEqual(create_refund(transport, "ch_1", 100)[1]["amount"], 100)

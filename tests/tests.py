import unittest
from pywindsorai.client import Client


class TestRequest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRequest, self).__init__(*args, **kwargs)
        self.bad_token = Client("abc-token")
        self.good_token = Client("")
        self.error_responses = [400, 401, 402, 403, 404]

    def test_fail_request(self):
        self.bad_token.connectors(date_preset="last_7d", fields=["account_name", "campaign"])
        self.assertIn(self.bad_token.status_code, self.error_responses)

    def test_success_request(self):
        self.good_token.connectors(date_preset="last_7d", fields=["account_name", "campaign"])
        self.assertEqual(self.good_token.status_code, 200)

    def test_non_existent_fields(self):
        dataset = self.good_token.connectors(date_preset="last_7d", fields=["field1", "field2"])
        self.assertEqual(len(dataset["data"]), 0)

    def test_some_existing_fields(self):
        dataset = self.good_token.connectors(date_preset="last_7d", fields=["account_name", "random_field"])
        self.assertGreaterEqual(len(dataset["data"]), 0)

    def test_random_date(self):
        dataset = self.good_token.connectors(date_preset="lcast_7d", fields=["account_name", "campaign"])
        self.assertIn(self.good_token.status_code, self.error_responses)

    def test_google_connector(self):
        dataset = self.good_token.connectors(
            connector="google_ads",
            date_preset="last_7d",
            fields=["account_name", "campaign", "clicks", "datasource", "source", "spend"]
        )
        self.assertEqual(self.good_token.status_code, 200)

    def test_non_existent_connector(self):
        dataset = self.good_token.connectors(
            connector="random_connector",
            date_preset="last_7d",
            fields=["account_name", "campaign", "clicks", "datasource", "source", "spend"]
        )
        self.assertIn(self.good_token.status_code, self.error_responses)

    def test_bad_token_list_connectors(self):
        self.bad_token.list_connectors
        self.assertEqual(self.bad_token.status_code, 200)

    def test_good_token_list_connectors(self):
        self.good_token.list_connectors
        self.assertEqual(self.good_token.status_code, 200)


if __name__ == "__main__":
    unittest.main()
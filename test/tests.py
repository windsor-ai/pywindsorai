import os
import unittest

from pywindsorai.client import Client
from pywindsorai import WindsorAIError, AuthenticationError


class TestRequest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRequest, self).__init__(*args, **kwargs)
        self.bad_token = Client("abc-token")
        self.good_token = Client(os.environ.get("WINDSOR_TOKEN"))

    def assert_successful_response(self, response):
        self.assertIsInstance(response, dict)
        self.assertIn('data', response)
        self.assertIsInstance(response['data'], list)

    def test_fail_request(self):
        with self.assertRaises(AuthenticationError):
            self.bad_token.connectors(date_preset="last_7d", fields=["account_name", "campaign"])

    def test_success_request(self):
        response = self.good_token.connectors(date_preset="last_7d", fields=["account_name", "campaign"])
        self.assert_successful_response(response)

    def test_non_existent_fields(self):
        response = self.good_token.connectors(date_preset="last_7d", fields=["field1", "field2"])
        self.assert_successful_response(response)
        self.assertEqual(len(response["data"]), 0)

    def test_some_existing_fields(self):
        response = self.good_token.connectors(date_preset="last_7d", fields=["account_name", "random_field"])
        self.assert_successful_response(response)
        self.assertGreaterEqual(len(response["data"]), 0)

    def test_random_date(self):
        with self.assertRaises(WindsorAIError):
            self.good_token.connectors(date_preset="lcast_7d", fields=["account_name", "campaign"])

    def test_google_connector(self):
        response = self.good_token.connectors(
            connector="google_ads",
            date_preset="last_7d",
            fields=["account_name", "campaign", "clicks", "datasource", "source", "spend"]
        )
        self.assert_successful_response(response)

    def test_non_existent_connector(self):
        with self.assertRaises(WindsorAIError):
            self.good_token.connectors(
                connector="random_connector",
                date_preset="last_7d",
                fields=["account_name", "campaign", "clicks", "datasource", "source", "spend"]
            )

    def test_bad_token_list_connectors(self):
        # list_connectors now returns List[str] directly
        connectors = self.bad_token.list_connectors
        self.assertIsInstance(connectors, list)

    def test_good_token_list_connectors(self):
        connectors = self.good_token.list_connectors
        self.assertIsInstance(connectors, list)

    def test_no_date(self):
        response = self.good_token.connectors(
            connector="google_ads",
            fields=["account_name", "campaign", "clicks", "datasource", "source", "spend"]
        )
        self.assert_successful_response(response)

    def test_from_date(self):
        response = self.good_token.connectors(
            connector="google_ads",
            date_from="2022-10-18",
            fields=["account_name", "campaign", "clicks", "datasource", "source", "spend", "date"]
        )
        self.assert_successful_response(response)

    def test_invalid_from_date(self):
        with self.assertRaises(WindsorAIError):
            self.good_token.connectors(
                connector="google_ads",
                date_from="208a",
                fields=["account_name", "campaign", "clicks", "datasource", "source", "spend", "date"]
            )

    def test_from_to_date(self):
        response = self.good_token.connectors(
            connector="google_ads",
            date_from="2022-10-18",
            date_to="2022-10-20",
            fields=["account_name", "campaign", "clicks", "datasource", "source", "spend", "date"]
        )
        self.assert_successful_response(response)


if __name__ == "__main__":
    unittest.main()

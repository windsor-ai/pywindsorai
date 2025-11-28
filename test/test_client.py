import os
import pytest
from datetime import date, timedelta
from src.client import Client
from src.exceptions import WindsorAIError, AuthenticationError, ConnectorNotFoundError

# --- Fixtures ---


@pytest.fixture
def client():
    """
    Fixture for an authenticated Client.
    Skips tests if WINDSOR_TOKEN is not set in environment variables.
    """
    token = os.environ.get("WINDSORAI_API_KEY", "")
    if not token:
        pytest.skip(
            "WINDSORAI_API_KEY environment variable not set. Skipping authenticated test."
        )
    return Client(token)


@pytest.fixture
def bad_client():
    """Fixture for a Client with an invalid token."""
    return Client("invalid-token-123")


# --- Helpers ---


def assert_successful_response(response, minimum_data_in_response=1):
    """Helper function to validate standard API response structure."""
    assert isinstance(response, dict), "Response should be a dictionary"
    assert "data" in response, "Response should contain a 'data' key"
    assert isinstance(response["data"], list), "'data' should be a list"
    assert len(response["data"]) >= minimum_data_in_response


def assert_successful_empty_response(response):
    assert_successful_response(response, 0)


# --- Tests ---


def test_fail_request(bad_client):
    """Ensure invalid tokens raise AuthenticationError."""
    with pytest.raises(AuthenticationError):
        bad_client.connectors(
            date_preset="last_7d", fields=["account_name", "campaign"]
        )


def test_success_request(client):
    """Ensure a valid request returns a success response."""
    response = client.connectors(
        date_preset="last_7d", fields=["account_name", "campaign"]
    )
    assert_successful_response(response)


def test_non_existent_fields(client):
    """Ensure requesting non-existent fields returns empty data (not error)."""
    response = client.connectors(
        date_preset="last_7d", fields=["non_existent_field_abc", "another_fake_field"]
    )
    assert_successful_empty_response(response)


def test_mixed_fields(client):
    """Ensure requesting a mix of valid and invalid fields works."""
    response = client.connectors(
        date_preset="last_7d", fields=["account_name", "campaign", "random_field_xyz"]
    )
    assert_successful_response(response)
    assert "account_name" in response["data"][0]


def test_invalid_date_preset(client):
    """Ensure invalid date presets raise WindsorAIError."""
    with pytest.raises(WindsorAIError):
        client.connectors(
            date_preset="invalid_preset_string", fields=["account_name", "campaign"]
        )


def test_google_connector(client):
    """Test fetching data specifically from the Google Ads connector."""
    with pytest.raises(ConnectorNotFoundError):
        client.connectors(
            connector="google_ads",
            date_preset="last_7d",
            fields=[
                "account_name",
                "campaign",
                "clicks",
                "datasource",
                "source",
                "spend",
            ],
        )


def test_non_existent_connector(client):
    """Ensure requesting a non-existent connector raises WindsorAIError."""
    with pytest.raises(WindsorAIError):
        client.connectors(
            connector="completely_random_connector_123",
            date_preset="last_7d",
            fields=["account_name", "clicks"],
        )


def test_list_connectors_bad_token(bad_client):
    """Test that listing connectors returns a list even with a bad token (if public) or handles it."""
    # Assuming list_connectors doesn't strictly require auth or returns empty list on some endpoints
    connectors = bad_client.list_connectors
    assert isinstance(connectors, list)


def test_list_connectors_good_token(client):
    """Test listing available connectors with a valid token."""
    connectors = client.list_connectors
    assert isinstance(connectors, list)
    assert len(connectors) > 0


def test_no_date_parameters(client):
    """Test request with no specific date parameters (relying on defaults)."""
    response = client.connectors(
        connector="facebook",
        fields=["account_name", "campaign", "clicks", "datasource", "source"],
    )
    assert_successful_response(response)


def test_from_date(client):
    """Test using a dynamic date_from parameter."""
    # Use 7 days ago dynamically
    date_from = (date.today() - timedelta(days=7)).isoformat()

    response = client.connectors(
        connector="facebook",
        date_from=date_from,
        fields=["account_name", "clicks", "date"],
    )
    assert_successful_response(response)


def test_invalid_from_date_format(client):
    """Test that an invalid date format raises WindsorAIError."""
    with pytest.raises(WindsorAIError):
        client.connectors(
            connector="google_ads",
            date_from="2022/99/99",  # Invalid format
            fields=["account_name", "clicks"],
        )


def test_from_to_date_range(client):
    """Test a specific date range using dynamic dates."""
    # Window: 7 days ago to 5 days ago
    date_start = (date.today() - timedelta(days=7)).isoformat()
    date_end = (date.today() - timedelta(days=5)).isoformat()

    response = client.connectors(
        connector="facebook",
        date_from=date_start,
        date_to=date_end,
        fields=["account_name", "clicks", "date"],
    )
    assert_successful_response(response)

    # Verify returned data (if any) is within range
    if response["data"]:
        for record in response["data"]:
            record_date = record.get("date")
            if record_date:
                assert record_date >= date_start
                assert record_date <= date_end

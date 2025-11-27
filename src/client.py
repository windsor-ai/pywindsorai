import requests
from typing import List, Union, Generator

from .exceptions import (
    WindsorAIError,
    AuthenticationError,
    RateLimitExceeded,
    NotFoundError,
    ServerError,
)
from .models import Filter


class Client:
    """
    Represents an API Client object for windsor.ai's APIs.
    """

    API_URL = "https://connectors.windsor.ai"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {"Accept": "application/json", "User-Agent": "windsorai/python/2.0.0"}
        )
        return session

    def _create_api_uri(self, path: str) -> str:
        return f"{self.API_URL}/{path}"

    def _handle_response(self, response: requests.Response) -> dict:
        """
        Parses response and raises exceptions for error codes.
        """
        if response.status_code == 200:
            return response.json()

        error_msg = f"HTTP {response.status_code}"
        try:
            payload = response.json()
            if "error" in payload:
                # Handle nested error objects or string messages
                err = payload["error"]
                if isinstance(err, dict):
                    error_msg = err.get("message", str(err))
                else:
                    error_msg = str(err)
        except ValueError:
            payload = response.text

        if response.status_code == 401:
            raise AuthenticationError("Invalid API Key.", 401, payload)
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {error_msg}", 404, payload)
        if response.status_code == 429:
            raise RateLimitExceeded("Rate limit exceeded.", 429, payload)
        if response.status_code >= 500:
            raise ServerError(
                f"Server Error: {error_msg}", response.status_code, payload
            )

        raise WindsorAIError(error_msg, response.status_code, payload)

    def _get(self, path: str, params: dict | None = None) -> dict:
        uri = self._create_api_uri(path)
        if params is None:
            params = {}

        params["api_key"] = self.api_key

        try:
            response = self.session.get(uri, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WindsorAIError(f"Connection error: {str(e)}")

    @property
    def list_connectors(self) -> List[str]:
        """
        Fetch list of all available connectors.
        """
        response = self._get(path="list_connectors")
        return response.get("data", [])

    def get_connector_fields(self, connector: str) -> List[dict]:
        """
        Get all available fields for a specific connector.

        Args:
            connector: The ID of the connector (e.g., 'facebook', 'google_ads')
        Returns:
            List of field definition dictionaries.
        """
        response = self._get(path=f"{connector}/fields")
        return response.get("data", [])

    def connectors(
        self,
        connector: str = "all",
        fields: List[str] | None = None,
        date_preset: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        filters: Union[List[Filter], Filter, List[list]] | None = None,
        refresh_since: str | None = None,
        refresh_interval: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        **kwargs,
    ) -> dict:
        """
        Fetch data from Windsor.ai.

        Args:
            connector: Connector ID (default: "all").
            fields: List of field names to retrieve.
            date_preset: E.g., 'last_7d', 'last_30d'.
            date_from: Start date (YYYY-MM-DD).
            date_to: End date (YYYY-MM-DD).
            filters: A Filter object, list of Filter objects, or raw list logic.
            refresh_since: E.g. '3d'. Window to refresh from upstream.
            refresh_interval: E.g. '6h'. How often to refresh upstream.
            limit: Max records to return.
            offset: Number of records to skip.

        Returns:
            Dictionary containing 'data' (list) and 'meta' (pagination info).
        """
        params = kwargs.copy()

        if fields:
            params["fields"] = ",".join(fields)

        if date_preset:
            params["date_preset"] = date_preset

        if date_from:
            params["date_from"] = date_from

        if date_to:
            params["date_to"] = date_to

        if filters:
            params["filter"] = Filter.to_json(filters)

        if refresh_since:
            params["refresh_since"] = refresh_since

        if refresh_interval:
            params["refresh_interval"] = refresh_interval

        if limit is not None:
            params["limit"] = limit

        if offset is not None:
            params["offset"] = offset

        return self._get(connector, params=params)

    def stream_connectors(
        self, connector="all", chunk_size=1000, **kwargs
    ) -> Generator[dict, None, None]:
        """
        Yields records one by one, automatically handling pagination.

        Args:
            connector: Connector ID.
            chunk_size: How many records to fetch per request.
            **kwargs: Arguments passed to .connectors() (fields, dates, etc.)
        """
        offset = 0
        while True:
            # Override limit/offset for the loop
            response = self.connectors(
                connector=connector, limit=chunk_size, offset=offset, **kwargs
            )

            data = response.get("data", [])
            if not data:
                break

            for record in data:
                yield record

            if len(data) < chunk_size:
                break

            offset += chunk_size

import requests
import time


class Client(object):
    """
    Represents an API Client object for windsor.ai's APIs.
    """

    API_URL = 'https://connectors.windsor.ai'

    def __init__(self, api_key):

        self.API_KEY = api_key
        self.session = self._init_session()

    def _init_session(self):

        session = requests.session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'windsorai/python'})
        return session

    def _create_api_uri(self, path):
        return self.API_URL + '/' + path

    def _request(self, method, path, signed, **kwargs):
        uri = self._create_api_uri(path)

        kwargs['params']['api_key'] = self.API_KEY

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Internal helper for handling API responses from the windsor.ai server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        # Any windsor.ai specific error handling can be done here
        # Nothing as such for now

        return response.json()

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request('delete', path, signed, **kwargs)

    # General Endpoints

    def connectors(self, **params):
        """
        Get data from one of the available windsor connectors.
        https://connectors.windsor.ai/#operations-default-get_connector

        Example usage:
            from pywindsorai.enums import LAST_7D
            from pywindsorai.fields import FIELD_SOURCE, FIELD_CAMPAIGN, FIELD_CLICKS

            client = Client(api_key)
            orders = client.connectors(date_preset=LAST_7D, fields=[FIELD_SOURCE, FIELD_CAMPAIGN, FIELD_CLICKS])

        :param params:
            date_preset - It's recommended that you use provided enums, instead of a hardcoded string. Example: LAST_7D
            fields - List of fields. It's recommended that you use FIELD_* enums, instead of hardcoded strings. Example: [FIELD_SOURCE, FIELD_CAMPAIGN, FIELD_CLICKS].
        :return:
        """

        # Python interface is a list. Whereas the API expects a comma seperated string.
        params['fields'] = ','.join(params['fields'])

        return self._get('all', params=params)

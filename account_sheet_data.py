
import json
import requests

class LarkSuiteCredentialsFetcher:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        url = 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'app_id': self.app_id,
            'app_secret': self.app_secret
        }
        print("Waiting for response from lark base")
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        print("Response Recieved")
        return response.json()['tenant_access_token']

    def fetch_credentials(self):
        url = 'https://open.larksuite.com/open-apis/bitable/v1/apps/AmtqbJV4raGoSYs7xInuIxP8sXg/tables/tbldOHKaqXLDEw4W/records'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        print("Getting lark base data")
        params = {'view_id': 'vew4skJySB', 'field_names': '["Restaurant name", "Invoice Email Address", "Address", "Payment_Amount", "Payment_date", "Payment_Confirmation_Number", "Date- start", "Date End"]'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        items = data['data']['items']
        print("Got Lark Base data")
        return items



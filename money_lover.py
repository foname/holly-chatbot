import requests
from base64 import b64encode, b64decode 
import re

class MoneyLover:

    def __init__(self, access_token=None):
        self.access_token = access_token

    @staticmethod
    def request_token(username, password):
        url = "https://web.moneylover.me/api/user/login-url"
        login_url = requests.request("POST", url)

        url= "https://oauth.moneylover.me/token"
        headers = {
            'Authorization': 'Bearer {}'.format(login_url.json()['data']['request_token']),
            'client': re.split("client=(.+?)&", login_url.json()['data']['login_url'])[1]
        }
        body= { "email": username, "password": password }
        response = requests.request("POST", url, headers=headers, data=body)
        if not response.json()['status']:
            return response.json()['message']
        return response.json()['access_token']

    def logout(self):
        self.access_token = None

    def _post_request(self, path, body=None, header=None):
        url = "https://web.moneylover.me/api{}".format(path)
        headers = {
            'Authorization': 'AuthJWT {}'.format(self.access_token)
        }
        if header:
            headers.update(header)
        print(headers)
        response = requests.request("POST", url, headers=headers, data=body)
        if response.json()['error']:
            return response.json()['msg']
        return response.json()['data']

    def get_user_info(self):
        return self._post_request('/user/info')

    def get_categories(self, wallet_id):
        header = { 'Content-Type': 'application/x-www-form-urlencoded' }
        body = { 'walletId': wallet_id }
        return self._post_request('/category/list', body, header)

    def get_wallets(self):
        return self._post_request('/wallet/list')

    def get_wallet_detail(self, wallet_id):
        wallets = self.get_wallets()
        for wallet in wallets:
            if wallet['_id'] == wallet_id:
                return wallet
        return wallets

    def get_wallet_names(self):
        wallets = self.get_wallets()
        return [ {wallet['name']: wallet['balance']}for wallet in wallets]

    def get_transaction(self):
        pass

    def add_transaction(self):
        pass


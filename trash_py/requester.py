# 負責發送請求，
# 負責處理伺服器回應。

import requests
from .config import API_URL, API_KEY, SECRET_KEY
from .signer import get_sign

def send_request(method, path, params, payload=None):
    url_params = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = get_sign(SECRET_KEY, url_params)
    url = f"{API_URL}{path}?{url_params}&signature={signature}"
    headers = {'X-BX-APIKEY': API_KEY}
    response = requests.request(method, url, headers=headers, data=payload)
    return response.json()

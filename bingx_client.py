# 初稿：將 BingX 價格查詢、開倉、關倉行為物件化封裝

import time
import requests
import hmac
import json
from hashlib import sha256

class BingXClient:
    def __init__(self, api_key, secret_key):
        self.APIURL = "https://open-api.bingx.com"
        self.APIKEY = api_key
        self.SECRETKEY = secret_key

    # 得到時間戳
    def _get_timestamp(self):
        return str(int(time.time() * 1000))

    # 用加密機加密資料
    def _sign(self, payload):
        key_bytes = self.SECRETKEY.encode("utf-8")
        payload_bytes = payload.encode("utf-8")
        signature = hmac.new(key_bytes, payload_bytes, digestmod=sha256).hexdigest()
        return signature

    # 發送的信件封裝區
    def _send_request(self, method, path, params_map, payload=None):
        params = "&".join([f"{k}={params_map[k]}" for k in sorted(params_map)])
        params += f"&timestamp={self._get_timestamp()}"
        signature = self._sign(params)
        url = f"{self.APIURL}{path}?{params}&signature={signature}"

        headers = {'X-BX-APIKEY': self.APIKEY}
        response = requests.request(method, url, headers=headers, data=payload or {})
        return response.json()

    # 查價
    def get_price(self, symbol="XAUT-USDT"):
        path = '/openApi/swap/v1/ticker/price'
        params = {"symbol": symbol}
        data = self._send_request("GET", path, params)
        return float(data['data']['price']) if data.get("code") == 0 else None
      
    # 開倉
    def place_order(self, symbol, side, position_side, quantity, take_profit_price=None):
        path = '/openApi/swap/v2/trade/order'
        params = {
            "symbol": symbol,
            "side": side,
            "positionSide": position_side,
            "type": "MARKET",
            "quantity": quantity
        }
        if take_profit_price:
            params["takeProfit"] = json.dumps({
                "type": "TAKE_PROFIT_MARKET",
                "stopPrice": take_profit_price,
                "price": take_profit_price,
                "workingType": "MARK_PRICE"
            })
        return self._send_request("POST", path, params)

    # 紀錄倉位號碼
    def get_position_id(self, symbol):
        path = "/openApi/swap/v2/user/positions"
        params = {"symbol": symbol}
        data = self._send_request("GET", path, params)
        try:
            return data["data"]["positionId"]
        except:
            return None

    # 關倉
    def close_position(self, order_id, symbol):
        path = "/openApi/swap/v2/trade/order"
        params = {
            "orderId": order_id,
            "symbol": symbol
        }
        return self._send_request("DELETE", path, params)

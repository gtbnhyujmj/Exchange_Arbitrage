# 第二版：新增 ArbitrageBot 套利策略封裝

import time
import requests
import hmac
import json
from hashlib import sha256

class ArbitrageBot:
    def __init__(self, bx_client, exb_client, config):
        self.bx = bx_client
        self.exb = exb_client
        self.symbol = config.get("symbol", "XAUT-USDT")
        self.check_interval = config.get("check_interval", 0.2)
        self.entry_spread = config.get("entry_spread", 5)
        self.add_spread_step = config.get("add_spread_step", 1)
        self.close_spread = config.get("close_spread", 0.5)
        self.entered = False
        self.last_spread = None
        self.entry_spread_value = None
        self.add_count = 0

    def run(self):
        while True:
            bx_price = self.bx.get_price(self.symbol)
            exb_price = self.exb.get_price(self.symbol)

            if bx_price is None or exb_price is None:
                print("⚠️ 價格獲取失敗，重試中...")
                time.sleep(self.check_interval)
                continue

            spread = bx_price - exb_price
            print(f"📈 BX: {bx_price}, B: {exb_price}, 差價: {spread:.2f}")

            if not self.entered:
                if abs(spread) >= self.entry_spread:
                    if spread > 0:
                        self.bx.place_order(self.symbol, "SELL", "SHORT", 1)
                        self.exb.place_order(self.symbol, "BUY", "LONG", 1)
                    else:
                        self.bx.place_order(self.symbol, "BUY", "LONG", 1)
                        self.exb.place_order(self.symbol, "SELL", "SHORT", 1)
                    self.entered = True
                    self.entry_spread_value = abs(spread)
                    self.last_spread = abs(spread)
            else:
                current_spread = abs(spread)

                if current_spread < self.last_spread - self.add_spread_step:
                    print(f"🔁 價差縮小，加碼第 {self.add_count + 1} 次")
                    if spread > 0:
                        self.bx.place_order(self.symbol, "SELL", "SHORT", 1)
                        self.exb.place_order(self.symbol, "BUY", "LONG", 1)
                    else:
                        self.bx.place_order(self.symbol, "BUY", "LONG", 1)
                        self.exb.place_order(self.symbol, "SELL", "SHORT", 1)
                    self.last_spread = current_spread
                    self.add_count += 1

                elif current_spread <= self.close_spread:
                    print("🏁 價差逼近 0，全部平倉")
                    pid = self.bx.get_position_id(self.symbol)
                    if pid:
                        self.bx.close_position(pid, self.symbol)
                    # exb 關倉略
                    break

            time.sleep(self.check_interval)

from bingx_client import BingXClient

APIKEY = "你的 API Key"
SECRETKEY = "你的 Secret Key"

# 建立 BingX 客戶端物件
bx = BingXClient(APIKEY, SECRETKEY)

# 查詢價格
price = bx.get_price("XAUT-USDT")
print("黃金現價:", price)

# 示範下單（請先確認參數安全再解開）
# bx.place_order("XAUT-USDT", "BUY", "LONG", 1)

# 查合約 ID
# pid = bx.get_position_id("XAUT-USDT")

# 平倉
# bx.close_position(pid, "XAUT-USDT")

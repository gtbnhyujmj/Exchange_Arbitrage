# Gold_Cross-Exchange-Arbitrage\
以黃金為標的，跨交易所搬磚套利。\
\
最後成果會是：\
bingx_client.py: 專門管理 BingX API 的請求\
exchangeB_client.py: 你未來對接的第二個交易所\
\
arbitrage_bot.py: 核心邏輯，負責策略、監控與決策\
main.py: 簡潔主程式，負責啟動執行\

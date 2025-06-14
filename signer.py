# 簽證機 = 加密機
# 放簽名/加密邏輯

import hmac
from hashlib import sha256

def get_sign(secret, payload):
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()

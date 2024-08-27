import requests
from plinko.settings import TELEGRAM_BOT_TOKEN, MINI_APP_URL

try:
    url = f"{MINI_APP_URL}/account/reset-users-pool"
    params = {
        "token": TELEGRAM_BOT_TOKEN,
    }

    resp = requests.get(url, data=params)
except:
    print('error , cant reset users pool')

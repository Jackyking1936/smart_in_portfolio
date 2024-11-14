#%%
import pickle
from pathlib import Path

from fubon_neo.sdk import FubonSDK, Mode, Order
from fubon_neo.constant import TimeInForce, OrderType, PriceType, MarketType, BSAction

my_file = Path("./info.pkl")
if my_file.is_file():
    with open('info.pkl', 'rb') as f:
        user_info_dict = pickle.load(f)
    
sdk = FubonSDK()
accounts = sdk.login(user_info_dict['id'], user_info_dict['pwd'], user_info_dict['cert_path'])
active_acc = accounts.data[0]
print(active_acc)
#%%

def handle_message(message):
    print(f'market data message: {message}')

sdk.init_realtime(Mode.Normal) # 建立行情連線

stock = sdk.marketdata.websocket_client.stock
stock.on('message', handle_message)
stock.connect()
stock.subscribe({ 
    'channel': 'aggregates', 
    'symbol': '2330'
})
# %%
from datetime import datetime

open_time = datetime.fromtimestamp(1729645202839875/1000000.0)
high_time = datetime.fromtimestamp(1729559210444302/1000000.0)
low_time = datetime.fromtimestamp(1729559542786817/1000000.0)
close_time = datetime.fromtimestamp(1729661400000000/1000000.0)

# print("現在是否收盤?", datetime.now() > close_time)
# %%
from threading import Timer

order_time = datetime.today().replace(hour=13, minute=25, second=0, microsecond=0)

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def check_for_order_time():
    if datetime.now()>order_time:
        print("make order")
    else:
        print("waiting")

timer = RepeatTimer(3, check_for_order_time)
timer.start()

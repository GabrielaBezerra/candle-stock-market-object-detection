import logging
from math import e
import time
from iqoptionapi.stable_api import IQ_Option
from matplotlib.pylab import f


class IQ:
    iq: IQ_Option

    def __init__(self):
        self.buy_dict = {}
        self.sell_dict = {}

    def login(self, verbose=True, iq=None, checkConnection=False):
        error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
        iqoption = IQ_Option("gabriela.hotdog@hotmail.com", "pdi123")
        check, reason = iqoption.connect()
        iqoption.change_balance("PRACTICE")
        if check:
            print("Start your robot")
            self.iq = iqoption
            # if see this you can close network for test
            # while True:
            #     if iqoption.check_connect() == False:  # detect the websocket is close
            #         print("try reconnect")
            #         check, reason = iqoption.connect()
            #         if check:
            #             print("Reconnect successfully")
            #         else:
            #             if reason == error_password:
            #                 print("Error Password")
            #             else:
            #                 print("No Network")
        else:
            if reason == "[Errno -2] Name or service not known":
                print("No Network")
            elif reason == error_password:
                print("Error Password")

    def buy(self, ACTIVES, cls):
        self.buy_dict[cls] = self.buy_dict.get(cls, 0) + 1
        self._operate("call", ACTIVES)

    def sell(self, ACTIVES, cls):
        self.sell_dict[cls] = self.sell_dict.get(cls, 0) + 1
        self._operate("put", ACTIVES)

    def _operate(self, ACTION, ACTIVES):
        print(f"Amount of sell {self.sell_dict}")
        print(f"Amount of buy {self.buy_dict}")
        print(f"Current balance ${self.iq.get_balance()}")

        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
        Money = 1
        expirations_mode = 1

        check, id = self.iq.buy(Money, ACTIVES, ACTION, expirations_mode)
        if check:
            print("!buy!", id) if ACTION == "call" else print("!sell!", id)
        else:
            print("buy fail:", id) if ACTION == "call" else print("sell fail:", id)

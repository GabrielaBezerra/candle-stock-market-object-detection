import logging
import csv
import time
from iqoptionapi.stable_api import IQ_Option


def atualizar_csv(file, dados):
    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(dados)


class IQ:
    iq: IQ_Option
    csv_file: str

    def __init__(self, csv_file):
        self.buy_dict = {}
        self.sell_dict = {}
        self.csv_file = csv_file

    def login(self, verbose=True, iq=None, checkConnection=False):
        error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
        iqoption = IQ_Option("seu_email_aqui", "sua_senha_aqui")
        check, reason = iqoption.connect()
        iqoption.change_balance("PRACTICE")
        if check:
            print("Start your robot")
            self.iq = iqoption
        else:
            if reason == "[Errno -2] Name or service not known":
                print("No Network")
            elif reason == error_password:
                print("Error Password")

        is_asset_open = iqoption.get_all_open_time()
        asset = "EURUSD-OTC"

        # verificar se o ativo está disponível
        if is_asset_open["binary"][asset]["open"]:
            print(f"O ativo {asset} está disponível para negociação.")
        else:
            print(f"O ativo {asset} não está disponível para negociação no momento.")
            print(is_asset_open["binary"])

    def buy(self, ACTIVES, cls):
        self.buy_dict[cls] = self.buy_dict.get(cls, 0) + 1
        self._operate("call", ACTIVES, cls)

    def sell(self, ACTIVES, cls):
        self.sell_dict[cls] = self.sell_dict.get(cls, 0) + 1
        self._operate("put", ACTIVES, cls)

    def _operate(self, ACTION, ACTIVES, cls):
        print(f"Amount of sell {self.sell_dict}")
        print(f"Amount of buy {self.buy_dict}")
        print(f"Current balance ${self.iq.get_balance()}")

        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
        Money = 1
        expirations_mode = 1

        check, id = self.iq.buy(Money, ACTIVES, ACTION, expirations_mode)
        if check:
            print("!buy!", id) if ACTION == "call" else print("!sell!", id)

            # geracao do relatorio
            horario = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            dados_negociacao = [
                id,
                ACTIVES,
                Money,
                expirations_mode,
                ACTION,
                str(self.iq.get_balance()).replace(".", ","),
                horario,
                cls.item(),
            ]
            atualizar_csv(self.csv_file, dados_negociacao)
        else:
            print("buy fail:", id) if ACTION == "call" else print("sell fail:", id)

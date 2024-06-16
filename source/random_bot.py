import time
import random
from iq import IQ
import csv

csv_file = 'random-negociacoes-' + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())) + '.csv'

with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["ID", "Ativo", "Valor Investido", "Tempo de Expiração", "Direção", "Balanco", "Horário", "Classe"])


iq = IQ(csv_file)

count = 0
# Loop
for _ in range(52):
    count += 1
    try:
        if not iq.iq.connect():
            iq.login()
    except:
        iq = IQ(csv_file)
        iq.login()

    random_sell_or_buy = random.choice(['buy', 'sell'])

    if random_sell_or_buy == 'sell':
        iq.sell("EURUSD-OTC", random_sell_or_buy)
    else:
        iq.buy("EURUSD-OTC", random_sell_or_buy)

    time.sleep(61)

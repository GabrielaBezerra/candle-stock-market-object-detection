import time
import random
import cv2
import screen
from bot import Bot
from iq import IQ
from ultralyticsplus import YOLO
import csv

# carregando o modelo
# https://huggingface.co/foduucom/stockmarket-pattern-detection-yolov8
model = YOLO("foduucom/stockmarket-pattern-detection-yolov8")

# configurando parâmetros do modelo
model.overrides["conf"] = 0.25  # NMS confidence threshold
model.overrides["iou"] = 0.5  # NMS IoU threshold
model.overrides["agnostic_nms"] = False  # NMS class-agnostic
model.overrides["max_det"] = 1000  # maximum number of detections per image

# setup arquivo do relatório
csv_file = (
    "negociacoes-" + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())) + ".csv"
)

with open(csv_file, mode="w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(
        [
            "ID",
            "Ativo",
            "Valor Investido",
            "Tempo de Expiração",
            "Direção",
            "Balanco",
            "Horário",
            "Classe",
        ]
    )

# setup Bot e login com selenium
bot = Bot()

# setup IQ API com arquivo csv para relatorio
iq = IQ(csv_file)
iq.login()

# controlando a frequencia de operações
last_trade_date = iq.iq.get_server_timestamp() - 60 * 1
last_box_cls = ""
last_x_right = 0
count = 0

# laço principal capturando frames e verificando conexao com API
while True:
    try:
        if not iq.iq.connect():
            iq.login()
    except:
        iq = IQ(csv_file)
        iq.login()

    # captura
    frame = screen.capture()

    # inferência
    results = model(frame, verbose=False)

    # visualização
    plot_results = results[0].plot()
    screen.show(plot_results)

    current_date = iq.iq.get_server_timestamp()

    # seleção da classe que será usada para tomada de decisão
    boxes = results[0].boxes
    filtered_boxes = [box for box in boxes if box.xywh[0][0] > 300]
    boxes_sorted_by_confidence = sorted(
        filtered_boxes, key=lambda box: box.conf, reverse=True
    )
    last_x_right -= 20
    for box in boxes_sorted_by_confidence:
        x_center = box.xywh[0, 0].item()
        width = box.xywh[0, 2].item()
        x_right = x_center + (width / 2)
        if last_x_right < x_right:
            last_box_cls = box.cls
            last_x_right = x_right

    # tomada de decisão e realização da operação
    if (
        current_date - last_trade_date > (60 * 1 + random.randint(-10, 10))
        and last_box_cls
    ):
        last_trade_date = current_date
        if last_box_cls in [1, 2]:
            iq.sell("EURUSD-OTC", last_box_cls)
        elif last_box_cls in [0, 5]:
            iq.buy("EURUSD-OTC", last_box_cls)
        else:
            print(f"unclear ${last_box_cls}")
        count += 1
    else:
        pass

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()

    if count == 60:
        cv2.destroyAllWindows()
        break

    time.sleep(5)

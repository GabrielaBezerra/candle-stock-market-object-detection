import time
import random
import cv2
import screen
from bot import Bot
from iq import IQ
from ultralyticsplus import YOLO
import csv

# load model
# https://huggingface.co/foduucom/stockmarket-pattern-detection-yolov8
model = YOLO("foduucom/stockmarket-pattern-detection-yolov8")

# set model parameters
model.overrides["conf"] = 0.25  # NMS confidence threshold
model.overrides["iou"] = 0.5  # NMS IoU threshold
model.overrides["agnostic_nms"] = False  # NMS class-agnostic
model.overrides["max_det"] = 1000  # maximum number of detections per image

csv_file = 'negociacoes-' + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())) + '.csv'

with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["ID", "Ativo", "Valor Investido", "Tempo de Expiração", "Direção", "Balanco", "Horário"])

bot = Bot()
iq = IQ(csv_file)
iq.login()

last_trade_date = iq.iq.get_server_timestamp() - 60 * 1
detected_patterns = []

last_box_cls = ''
last_x_right = 0

count = 0

# Loop through the video frames
while True:
    try:
        if not iq.iq.connect():
            iq.login()
    except:
        iq = IQ(csv_file)
        iq.login()

    # print(bot.driver.get_window_rect())

    # Read a frame from the video
    frame = screen.capture()

    # Run YOLOv8 inference on the frame
    results = model(frame, verbose=False)

    # Visualize the results on the frame
    plot_results = results[0].plot()
    screen.show(plot_results)

    # Get the boxes from the results
    boxes = results[0].boxes

    # Filter boxes which x position is over 300
    filtered_boxes = [box for box in boxes if box.xywh[0][0] > 300]
    boxes_sorted_by_confidence = sorted(
        filtered_boxes, key=lambda box: box.conf, reverse=True
    )

    last_x_right -= 20

    # For each box in the filtered boxes
    for box in boxes_sorted_by_confidence:
        x_center = box.xywh[0, 0].item()
        width = box.xywh[0, 2].item()

        x_right = x_center + (width / 2)
        if last_x_right < x_right:
            last_box_cls = box.cls
            last_x_right = x_right

    current_date = iq.iq.get_server_timestamp()

    # check if current_date is after 5 minutes of the last trade
    if current_date - last_trade_date > (60 * 1 + random.randint(-10, 10)) and last_box_cls:
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
        # print("You can't try to trade right now. Wait 5 minutes.")

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()

    if count == 50:
        cv2.destroyAllWindows()
        break

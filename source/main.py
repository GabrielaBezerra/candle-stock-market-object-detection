import random
import cv2
from matplotlib.pyplot import annotate
from sympy import plot
import screen
from bot import Bot
from iq import IQ
from ultralyticsplus import YOLO

# load model
# https://huggingface.co/foduucom/stockmarket-pattern-detection-yolov8
model = YOLO("foduucom/stockmarket-pattern-detection-yolov8")

# set model parameters
model.overrides["conf"] = 0.25  # NMS confidence threshold
model.overrides["iou"] = 0.5  # NMS IoU threshold
model.overrides["agnostic_nms"] = False  # NMS class-agnostic
model.overrides["max_det"] = 1000  # maximum number of detections per image

bot = Bot()
iq = IQ()
iq.login()

last_trade_date = iq.iq.get_server_timestamp() - 60 * 5
detected_patterns = []


# Loop through the video frames
while True:
    if not iq.iq.connect():
        id.login()

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

    # For each box in the filtered boxes
    for box in boxes_sorted_by_confidence:
        current_date = iq.iq.get_server_timestamp()
        # check if current_date is after 5 minutes of the last trade
        if current_date - last_trade_date > (60 * 5 + random.randint(-10, 10)):
            last_trade_date = current_date
            if box.cls in [1, 2]:
                iq.sell("USDBRL", box.cls)
            elif box.cls in [0, 5]:
                iq.buy("USDBRL", box.cls)
            else:
                print(f"unclear ${box.cls}")
        else:
            print("You can't try to trade right now. Wait 5 minutes.")

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()

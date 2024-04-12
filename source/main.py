import cv2
import screen
from bot import Bot
from ultralyticsplus import YOLO, render_result

# load model
# https://huggingface.co/foduucom/stockmarket-pattern-detection-yolov8
model = YOLO("foduucom/stockmarket-pattern-detection-yolov8")

# set model parameters
model.overrides["conf"] = 0.25  # NMS confidence threshold
model.overrides["iou"] = 0.45  # NMS IoU threshold
model.overrides["agnostic_nms"] = False  # NMS class-agnostic
model.overrides["max_det"] = 1000  # maximum number of detections per image

bot = Bot()

# Loop through the video frames
while True:
    print(bot.driver.get_window_rect())

    # # Read a frame from the video
    # frame = screen.capture()

    # # Run YOLOv8 inference on the frame
    # results = model(frame)

    # # Visualize the results on the frame
    # screen.show(results[0].plot())

    # if cv2.waitKey(25) & 0xFF == ord("q"):
    #     cv2.destroyAllWindows()

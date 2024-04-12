import cv2
import numpy as np
from PIL import ImageGrab
from ultralyticsplus import YOLO, render_result

# load model
model = YOLO("foduucom/stockmarket-pattern-detection-yolov8")

# set model parameters
model.overrides["conf"] = 0.25  # NMS confidence threshold
model.overrides["iou"] = 0.45  # NMS IoU threshold
model.overrides["agnostic_nms"] = False  # NMS class-agnostic
model.overrides["max_det"] = 1000  # maximum number of detections per image


def capture_dynamic():
    # Capture half of the window
    screen = ImageGrab.grab(bbox=(0, 0, 900, 1080))
    # screen = ImageGrab.grab(bbox=(0, 0, 1920, 1080))

    # Convert the screen to an array
    screen_array = np.array(screen)

    # Convert the array to an image
    screen_image = cv2.cvtColor(screen_array, cv2.COLOR_BGRA2BGR)

    return screen_image


# initialize video capture
# Open the video file

# Loop through the video frames
while True:
    # Read a frame from the video
    frame = capture_dynamic()

    # get width and size from frame
    height, width, _ = frame.shape

    # Setting the points for cropped image
    left = 0
    top = 400
    right = width
    bottom = height

    # Cropped image of above dimension
    # (It will not change original image)
    # frame = frame.crop((left, top, right, bottom))

    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    screen_grab = np.array(annotated_frame)

    image = cv2.resize(cv2.cvtColor(screen_grab, cv2.COLOR_RGB2BGRA), (900, 1080))
    # image = cv2.resize(cv2.cvtColor(screen_grab, cv2.COLOR_RGB2BGRA), (1920, 1080))
    cv2.imshow("YOLO Reference", image)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

import cv2
import numpy as np
from PIL import ImageGrab


def capture():
    # Capture half of the window
    screen = ImageGrab.grab(bbox=(0, 0, 900, 1080))
    # screen = ImageGrab.grab(bbox=(0, 0, 1920, 1080))

    # Convert the screen to an array
    screen_array = np.array(screen)

    # Convert the array to an image
    screen_image = cv2.cvtColor(screen_array, cv2.COLOR_BGRA2BGR)

    # get width and size from frame
    height, width, _ = screen_image.shape

    # Setting the points for cropped image
    left = 0
    top = 0
    right = width
    bottom = height

    # Cropped image of above dimension
    screen_image = screen_image[top:bottom, left:right]

    return screen_image


def show(annotated_frame):
    screen_grab = np.array(annotated_frame)

    image = cv2.resize(cv2.cvtColor(screen_grab, cv2.COLOR_RGB2BGRA), (900, 1080))
    # image = cv2.resize(cv2.cvtColor(screen_grab, cv2.COLOR_RGB2BGRA), (1920, 1080))

    cv2.imshow("YOLO Reference", image)

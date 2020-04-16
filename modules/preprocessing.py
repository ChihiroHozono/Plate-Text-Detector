import cv2
import numpy as np


def mask_img(img):
    hue_lower = 165
    hue_upper = 200

    return_img = np.full_like(img, 255, dtype=np.uint8)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i_row, row in enumerate(hsv_img):
        for i_column, column in enumerate(row):
            hue = column[0] * 2  # NOTE: OpenCVのHueの幅が0~179の為

            if (hue_lower <= hue) and (hue <= hue_upper):
                return_img[i_row][i_column] = np.array([0, 0, 0], dtype=np.uint8)
            else:
                continue

    return return_img

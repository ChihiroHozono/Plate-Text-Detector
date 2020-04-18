import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylsd.lsd import lsd

from modules.preprocess import (
    mask_img,
    noise_reduction,
    binalize,
    get_contour,
    get_plate_img,
)


if __name__ == "__main__":
    img_path = "/Users/Chihiro/Personal/10_Projects/GPC/get_plant_plate_txt/image/20200411_1.jpg"
    output_dir = "/Users/Chihiro/Desktop/"

    org_img = cv2.imread(img_path)
    img = cv2.imread(img_path)

    # プレート以外の箇所をマスク
    img = mask_img(img)
    img = noise_reduction(img)
    img = binalize(img)

    img = cv2.Canny(img, 10, 255, apertureSize=3)

    # 画像の膨張・縮小
    kernel = np.ones((5, 5), np.uint8)

    img = cv2.dilate(img, kernel, iterations=10)
    img = cv2.erode(img, kernel, iterations=3)

    # プレート四隅の座標取得
    contour = get_contour(org_img, img)
    get_plate_img(contour)

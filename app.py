import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylsd.lsd import lsd

import click
from modules.preprocess import (
    mask_img,
    noise_reduction,
    binalize,
    get_contour,
    get_plate_img,
)


@click.command()
@click.option("--img_path", required=True, type=str)
def main(img_path):
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
    contour = get_contour(output_dir, org_img, img)
    img = get_plate_img(org_img, contour)
    cv2.imwrite(f"{output_dir}plate_img.png", img)


if __name__ == "__main__":
    main()

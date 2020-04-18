import os

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
    get_edge,
)


@click.command()
@click.option("--output_dir", required=True, type=str)
@click.option("--input_img", required=True, type=str)
def main(output_dir, input_img):

    org_img = cv2.imread(input_img)
    processed_img = org_img
    basename = os.path.basename(input_img)
    file_name = os.path.splitext(basename)[0] + ".png"
    output_path = os.path.join(output_dir, file_name)

    img = mask_img(processed_img)
    img = noise_reduction(img)
    img = binalize(img)
    img = get_edge(img)
    contour = get_contour(img)
    img = get_plate_img(org_img, contour)
    cv2.imwrite(output_path, img)


if __name__ == "__main__":
    main()

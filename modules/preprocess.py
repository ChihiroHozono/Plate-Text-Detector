import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylsd.lsd import lsd

img_path = (
    "/Users/Chihiro/Personal/10_Projects/GPC/get_plant_plate_txt/image/20200411_1.jpg"
)
output_dir = "/Users/Chihiro/Desktop/"
org_img = cv2.imread(img_path)


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


def binalize(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #     img_gray = cv2.GaussianBlur(img_gray,(5,5),0)

    # 大津の二値化
    low_thr = 0
    hight_thr = 255
    retval, img_bin = cv2.threshold(img_gray, low_thr, hight_thr, cv2.THRESH_OTSU)

    #     適応的閾値処理による二値化
    #     img_bin = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 39,2)

    return img_bin


def get_contour(org_img, img):

    contours_img = org_img

    #   領域の抽出
    img, contours, hierarchy = cv2.findContours(
        img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    # 面積の表示
    contour_areas = {}
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        contour_areas[i] = area

    #     面積が最大のindexを取得（面積が大きすぎるものは省いた方が良い）
    #     max_area = sorted(contour_areas.values(),reverse=True)[0]
    max_area = max(contour_areas.values())
    max_area_idx = [i for i, v in contour_areas.items() if v == max_area][0]

    max_contour = contours[max_area_idx]
    arc_len = cv2.arcLength(max_contour, True)

    # 輪郭を近似
    approx_contour = cv2.approxPolyDP(max_contour, epsilon=0.05 * arc_len, closed=True)

    cv2.drawContours(contours_img, approx_contour, -1, (0, 255, 0), 30)
    cv2.imwrite(f"{output_dir}approx_contour.png", contours_img)

    return approx_contour


def noise_reduction(img):
    #     kernel = np.ones((10,10)) # カーネルサイズの調整が必要そう
    #     img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.medianBlur(img, 15)
    return img


# 歪み補正
def get_plate_img(contour):
    approx = contour.tolist()

    left = sorted(approx, key=lambda x: x[0])[:2]
    right = sorted(approx, key=lambda x: x[0])[2:]

    left_down = sorted(left, key=lambda x: x[0][1])[0]
    left_up = sorted(left, key=lambda x: x[0][1])[1]
    right_down = sorted(right, key=lambda x: x[0][1])[0]
    right_up = sorted(right, key=lambda x: x[0][1])[1]
    perspective_base = np.float32([left_down, right_down, right_up, left_up])
    perspective = np.float32([[0, 0], [700, 0], [700, 500], [0, 500]])

    psp_matrix = cv2.getPerspectiveTransform(perspective_base, perspective)
    img_psp = cv2.warpPerspective(org_img, psp_matrix, (700, 500))

    return img_psp

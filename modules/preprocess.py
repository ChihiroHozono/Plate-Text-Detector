import cv2
import numpy as np


def mask_img(img):
    masked_img = np.full_like(img, 255, dtype=np.uint8)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i_row, row in enumerate(hsv_img):
        for i_column, column in enumerate(row):
            hue = column[0] * 2  # NOTE: OpenCVのHueの幅が0~179の為

            if (100 <= hue) and (hue <= 200):
                masked_img[i_row][i_column] = np.array([0, 0, 0], dtype=np.uint8)
            else:
                continue

    return masked_img


def binalize(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 大津の二値化
    retval, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)

    return img_bin


def get_contour(img):

    #  領域の抽出
    img, contours, hierarchy = cv2.findContours(
        img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    # 面積の取得
    contour_areas = {}
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        contour_areas[i] = area

    # 面積が最大のindexを取得
    max_area = max(contour_areas.values())
    max_area_idx = [i for i, v in contour_areas.items() if v == max_area][0]

    max_contour = contours[max_area_idx]
    arc_len = cv2.arcLength(max_contour, True)

    # 輪郭を近似
    approx_contour = cv2.approxPolyDP(max_contour, epsilon=0.05 * arc_len, closed=True)

    return approx_contour


def noise_reduction(img):

    # 平滑化がないと領域抽出で、プレート内の文字領域を抽出してしまう。
    img = cv2.medianBlur(img, 15)

    # # 画像の膨張・縮小によるノイズ除去
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.dilate(img, kernel, iterations=7)
    img = cv2.erode(img, kernel, iterations=7)

    return img


def get_edge(img):
    img = cv2.Canny(img, 10, 255, apertureSize=3)
    return img


def get_plate_img(org_img, contour):
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

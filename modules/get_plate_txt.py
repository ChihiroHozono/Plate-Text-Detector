import os
from base64 import b64encode
import re
from sys import argv
import json
import requests


API_KEY = os.environ["GOOGLE_API_KEY"]


def _get_txt_from_img():

    ENDPOINT_URL = "https://vision.googleapis.com/v1/images:annotate"
    img_path = ["/Users/Chihiro/Desktop/edited_20200412_2.png"]
    output_path = "/Users/Chihiro/Desktop/edited_20200412_2.json"

    img_requests = []
    for imgname in img_path:
        with open(imgname, "rb") as f:
            ctxt = b64encode(f.read()).decode()
            img_requests.append(
                {
                    "image": {"content": ctxt},
                    "features": [{"type": "TEXT_DETECTION", "maxResults": 5}],
                }
            )

    response = requests.post(
        ENDPOINT_URL,
        data=json.dumps({"requests": img_requests}).encode(),
        params={"key": API_KEY},
        headers={"Content-Type": "application/json"},
    )

    for idx, resp in enumerate(response.json()["responses"]):
        # レスポンスの出力
        with open(output_path, "w") as f:
            json.dump(resp, f, indent=2, ensure_ascii=False)


def get_txt_from_ocr_result():
    ocr_result_path = "/Users/Chihiro/Desktop/edited_20200412_2.json"

    new_txt = []
    with open(ocr_result_path) as f:
        ocr_result = json.load(f)
        txt = ocr_result["textAnnotations"][0]["description"]

    txt = txt.split("\n")
    new_txt = []

    for row in txt:
        row_cnt_without_hiragana = len(re.sub("[ぁ-ん ]", "", row))
        if row_cnt_without_hiragana == 0:
            continue
        elif re.match("[a-zA-Z.]", row):
            new_txt.append(row)
        else:
            row = row.replace(" ", "")
            new_txt.append(row)

    print(new_txt)


if __name__ == "__main__":
    get_txt_from_ocr_result()

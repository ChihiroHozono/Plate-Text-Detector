from PIL import ExifTags, Image

img_path = "/Users/Chihiro/Personal/10_Projects/GPC/Plate-Text-Detector/image/20200412_exif.jpg"

img = Image.open(img_path)
exif = img._getexif()


gps_tag = None

for tag_id, value in exif.items():
    tag = ExifTags.TAGS[tag_id]
    if tag == "GPSInfo":
        gps_tag = tag_id
        break

gps_info = {}
for i, v in exif[gps_tag].items():
    gps_tag_c = ExifTags.GPSTAGS[i]
    gps_info[gps_tag_c] = v


def conv_deg(v):
    # 分数を度に変換
    d = float(v[0][0]) / float(v[0][1])
    m = float(v[1][0]) / float(v[1][1])
    s = float(v[2][0]) / float(v[2][1])
    return d + (m / 60.0) + (s / 3600.0)


latitiude = gps_info["GPSLatitude"]
longitude = gps_info["GPSLongitude"]

print(conv_deg(latitiude))
print(conv_deg(longitude))

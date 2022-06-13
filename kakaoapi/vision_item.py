import requests
from PIL import Image, ImageDraw
from io import BytesIO

REST_API_KEY = open("key.txt", "r").read().strip()

VISION_API_URL = "https://dapi.kakao.com/v2/vision/product/detect"

def detect_product(image_url):
  headers = {
    "Authorization": f"KakaoAK {REST_API_KEY}",
  }
  data = {
    "image_url": image_url,
  }
  rsp = requests.post(VISION_API_URL, headers=headers, data=data)
  rsp_json = rsp.json()
  return rsp_json

def show_products(image_url, detection_result):
  image_rsp = requests.get(image_url)
  file_jpgdata = BytesIO(image_rsp.content)
  image = Image.open(file_jpgdata)

  draw = ImageDraw.Draw(image)
  for obj in detection_result["result"]["objects"]:
    x1 = int(obj["x1"] * image.width)
    y1 = int(obj["y1"] * image.height)
    x2 = int(obj["x2"] * image.width)
    y2 = int(obj["y2"] * image.height)
    # 사각형 그리기
    draw.rectangle((x1, y1, x2, y2), fill=None, outline="red", width=2)
    draw.text((x1+5, y1+5), obj["class"], (255, 255, 0))
  del draw

  return image

if __name__ == "__main__":
  IMAGE_URL = "https://imgnews.pstatic.net/image/001/2022/06/14/PAP20220613128201009_P4_20220614011208539.jpg?type=w647"

  detection_result = detect_product(IMAGE_URL)
  image = show_products(IMAGE_URL, detection_result)
  image.show()

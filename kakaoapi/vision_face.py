import requests
from PIL import Image, ImageFilter

REST_API_KEY = open("key.txt", "r").read().strip()

VISION_API_URL = "https://dapi.kakao.com/v2/vision/face/detect"

def detect_face(filename):
  headers = {
    "Authorization": f"KakaoAK {REST_API_KEY}",
  }
  files = {
    "image": open("zelenskiy.jpg", "rb"),
  }
  rsp = requests.post(VISION_API_URL, headers=headers, files=files)
  rsp_json = rsp.json()
  return rsp_json

def mosaic(filename, detection_result):
  image = Image.open(filename)

  for face in detection_result["result"]["faces"]:
    x = int(face["x"] * image.width)
    y = int(face["y"] * image.height)
    w = int(face["w"] * image.width)
    h = int(face["h"] * image.height)
    print(f"Face location: ({x}, {y}), ({x+w}, {y+h})")
    box = image.crop((x, y, x+w, y+h))
    # 모자이크 처리
    box = box.resize((20, 20), Image.Resampling.NEAREST).resize((w, h), Image.Resampling.NEAREST)
    image.paste(box, (x, y, x+w, y+h))
  
  return image

if __name__ == "__main__":
  IMAGE = "zelenskiy.jpg"
  detection_result = detect_face(IMAGE)
  image = mosaic(IMAGE, detection_result)
  image.show()

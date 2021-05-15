import cv2
import base64
import requests


def pic_save(path):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(path, frame)
    print("存储成功")


def pic_get(path):
    with open(path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
        return img_stream


def pic_Compared(path1,path2):
    original_image = pic_get(path1)
    new_image = pic_get(path2)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    params =[
            {
                "image": original_image,
                "image_type": "BASE64",
                "face_type": "LIVE",
                "quality_control": "LOW",
                "liveness_control": "LOW"
            },
            {
                "image": new_image,
                "image_type": "BASE64",
                "face_type": "LIVE",
                "quality_control": "LOW",
                "liveness_control": "LOW"
            }
    ]

    access_token = '[24.64704f2c3286bc5a63ddb8418600f9af.2592000.1623661342.282335-24172054]'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, json=params, headers=headers)
    if response:
        out = response.json()
        if out['error_msg']=="SUCCESS" and int(out['result']['score'])>80:
            print("成功了")
            return 'success'
        else:
            return "false"
    else:
        print("搞错啦")
        return "false"

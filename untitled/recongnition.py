from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from aip import AipFace
import base64
import json

from PIL import Image
from PIL import ImageDraw

#百度接口信息
APP_ID = '16877761'
API_KEY = '6VGRZgAOaBn49GdMKozwbwAP'
SECRET_KEY = 'y4BMHKlpjUvBSDRO8wIpW9Y7d2fAjOFX'
client = AipFace(APP_ID,API_KEY,SECRET_KEY)
imageType = "BASE64"

#定义参数变量
options = {}
options["max_face_num"] = 1
options["face_field"] = "age,beauty,gender,landmark"

def recognition_post(request):
    context ={}    #此处将原文的content改为context，下同
    if request.POST:
        with open(".\\static\\images\\" +str(request.FILES['Photo']),"rb") as f:     #所有路径均为绝对路径，下同
            base64_date = base64.b64encode(f.read())
            image = str(base64_date,encoding='utf-8');
            result = client.detect(image, imageType, options)


        context['Photo'] = "\\static\\iamges\\"+str(request.FILES['Photo'])

#将百度接口返回的数据转成json对象
        json_str = json.dumps(result)

#对数据进行解码
        json_data = json.loads(json_str)

        context['age'] = json_data['result']['face_list'][0]['age']
        context['beauty'] = json_data['result']['face_list'][0]['beauty']
        gender = json_data['result']['face_list'][0]['gender']['type']
        if gender == 'female':
            context['gender'] = "女性"
        else:
            context['gender'] = "男性"
        landmark72 = json_data['result']['face_list'][0]['landmark72']

        im1=Image.open(".\\static\\images\\"+str(request.FILES['Photo']))
        draw = ImageDraw.Draw(im1)
        for index in range(72):
            xy = landmark72[index]
            draw.text((xy['x'],xy['y']),"o",(255,255,0))
        draw = ImageDraw.Draw(im1)
        im1.save("static\\images\\target_img.jpg")
        context['target_img'] = "static\\images\\target_img.jpg"


    return render(request, "view.html", context)

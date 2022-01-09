import requests
#from django.shortcuts import render
from django.shortcuts import redirect,render,reverse
from django.contrib import messages
from . import exception
from .models import Account
import json
import os 

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .gmail_send import gmail_send
from django.http import HttpResponse

# Create your views here.
domain = "http://58.142.223.232:8060/"

client_id = "" # 카카오 로그인 REST API KEY


# Create your views here.
def kakao_login(request):
    
    REDIRECT_URI =domain+ "users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
    )
    
    except KakaoException as error:
        messages.error(request, error)
        return redirect("kakao_login")

def kakao_login_callback(request):
    try:
    	#(1)
        code = request.GET.get("code")

        REDIRECT_URI = domain + "users/login/kakao/callback/"
        #(2)
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}")
        #(3)
        token_json = token_request.json()

        error = token_json.get("error", None)
        if error is not None:
            print(error)
        
        #(4)
        access_token = token_json.get("access_token")
        #(5)
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()        
        kakao_id = profile_json.get('id',None)
        
        if kakao_id is not None:
            email = profile_json.get('kakao_account')['email']
        
        if email == None:
            print(None)
        
        
        #(6)
        print("profile json:  ",profile_json)
        email = profile_json.get("kakao_account", None).get("email")
        
        if email is None:
            raise exception.KakaoException()

        #(7)
        # 카카오 로그인 성공한 경우
        try:
            user = Account.objects.get(user_id = email)
            
        except Account.DoesNotExist:
            print('최초가입\n DB에 이메일 저장 후 cctv 선택화면으로 넘기기')
            user_account = Account.objects.create(
                        user_id = email,
            )
            user_account.save()
            return(redirect("cctv:select_cctv"))
        except Exception as e:
            print(e)


        
        if user.cam_id is None:
            print("cam 설정안됨")
            return(redirect("cctv:select_cctv"))

        return redirect("cctv:main_page")
    
    except KeyError: 
        print('email 없음')
    except exception.KakaoException():
        return redirect("users:login")

def login(request):
    render(request, "users/login.html")


#@method_decorator(csrf_exempt, name="dispatch")
@csrf_exempt
def send_email(request):
    req_body = json.loads(request.body.decode('utf-8'))
    to = Cctv.objects.get(cam_id = req_body["cam_id"]).user_id

    gmail_send(to, req_body["space"], req_body["day"], req_body["time"], req_body["filename"])

    return HttpResponse("good")
    

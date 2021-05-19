import requests
#from django.shortcuts import render
from django.shortcuts import redirect,render,reverse
from django.contrib import messages
from . import exception

from .models import Account
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
domain = "http://192.168.0.15:8040/"
#domain = "http://localhost:8030/"

cid1 = '9606de62e75d3b6b41ce598441911359'
cid2 = 'a632e5f5e4017b7725e3ac3dbb86daa5'


client_id = cid1


def kakao_login(request):
    
    #try:
    #    if request.users.is_authenticated:
    #        raise SocailLoginException("User already logged in")
    #os.environ.get("KAKAO_ID")
    REDIRECT_URI =domain+ "users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
    )
    
    #except KakaoException as error:
    #    messages.error(request, error)
    #    return redirect("kakao_login")

    #except SocialLoginException as error:
    #    messages.error(request, error)
    #    return redirect("kakao_login")

def kakao_login_callback(request):
    try:
    	#(1)
        code = request.GET.get("code")
        #os.environ.get("KAKAO_ID")
        REDIRECT_URI = domain + "users/login/kakao/callback/"
        #(2)
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}")
        #(3)
        token_json = token_request.json()
        
        error = token_json.get("error", None)
        if error is not None:
            print(error)
        #    raise exception.KakaoException()
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
        
        
        #if Account.objects.get(
        #(6)
        #print("profile json:  ",profile_json)
        #email = profile_json.get("kakao_account", None)#.get("email")
        #print('email:  ',email)
        #if email is None:
        #    raise exception.KakaoException()
        #properties = profile_json.get("properties")
        #nickname = properties.get("nickname")
        #profile_image = properties.get("profile_image")
        #(7)
        
        # 카카오 로그인 성공한 경우
        try:
            #user = Account.objects.get_or_none(user_id = email)
            """
            if user is None:
                print('최초가입\n DB에 이메일 저장 후 cctv 선택화면으로 넘기기')
            user_account = Account.objects.create(
                        user_id = email,

            )
            user_account.save()
            """
            user = Account.objects.get(user_id = email)
            print('이메일: ',user.user_id,' 가입일: ',user.sign_up_date)
        except Account.DoesNotExist:
            print('최초가입\n DB에 이메일 저장 후 cctv 선택화면으로 넘기기')
            user_account = Account.objects.create(
                        user_id = email,

            )
            user_account.save()
        except Exception as e:
            print(e)


        """
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise exception.KakaoException()
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            #(8)
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        """
        #login(request, user)
        return redirect("cctv:index")
    except KeyError: # exception.KakaoException():
        print('email 없음')
        return redirect("users:login")

def login(request):
    render(request, "users/login.html")
    

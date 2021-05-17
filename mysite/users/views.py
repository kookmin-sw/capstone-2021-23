import requests
#from django.shortcuts import render
from django.shortcuts import redirect,render,reverse
from django.contrib import messages
from . import exception
# Create your views here.
domain = "http://192.168.0.10:8030/"
def kakao_login(request):
    
    #try:
    #    if request.users.is_authenticated:
    #        raise SocailLoginException("User already logged in")
    client_id = '9606de62e75d3b6b41ce598441911359'#os.environ.get("KAKAO_ID")
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
        client_id = '9606de62e75d3b6b41ce598441911359'#os.environ.get("KAKAO_ID")
        REDIRECT_URI = domain + "users/login/kakao/callback/"
        #(2)
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}")
        #(3)
        token_json = token_request.json()
        print(token_json)
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
    except exception.KakaoException():
        return redirect("users:login")

def login(request):
    render(request, "users/login.html")

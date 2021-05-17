from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    #path('', views.index, name='index'),
    path('login/kakao/', views.kakao_login, name='kakao-login'),
    path("login/kakao/callback/", views.kakao_login_callback, name="kakao-callback"),    
]

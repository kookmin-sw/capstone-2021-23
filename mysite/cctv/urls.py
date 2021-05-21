from django.urls import path
from . import views

# 리스트를 순회하며 일치하는 패턴을 찾을 때 까지 요청된 URL과 패턴을 비교
app_name = 'cctv'
urlpatterns =[
    # parameter
    # route, view, (kwargs, name)
    path('', views.index, name='index'),
    path('serveStreaming/', views.serveStreaming,name='serveStreaming'),
    # 첫 회원가입시 감시할 cctv 설정 페이지 경로
    path('registration/',views.select_cctv,name='select_cctv'),
    #path('', views.gen, name='gen')
]

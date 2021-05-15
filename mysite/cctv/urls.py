from django.urls import path
from . import views

# 리스트를 순회하며 일치하는 패턴을 찾을 때 까지 요청된 URL과 패턴을 비교
app_name = 'cctv'
urlpatterns =[
    # parameter
    # route, view, (kwargs, name)
    path('', views.index, name='index'),
    path('livefe/', views.livefe,name='livefe'),
    #path('', views.gen, name='gen')
]

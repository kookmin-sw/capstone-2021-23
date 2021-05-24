from django.db import models
from cctv.models import Cctv 
#import ..cctv.models import CCTV
class Account(models.Model):
    user_id = models.CharField(max_length= 30,unique=True)
    # auto_now_add : 최소 저장(insert)시에만 현재 날짜 저장
    sign_up_date = models.DateTimeField(auto_now_add=True)
    cam_id = models.ForeignKey(Cctv, related_name = "cctv", on_delete = models.SET_NULL, null = True, db_column = "cam_id")

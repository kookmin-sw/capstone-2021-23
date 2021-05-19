from django.db import models

class Account(models.Model):
    user_id = models.CharField(max_length= 20,unique=True)
    # auto_now_add : 최소 저장(insert)시에만 현재 날짜 저장
    sign_up_date = models.DateTimeField(auto_now_add=True)


from django.db import models

# Create your models here.

class Cctv(models.Model):
    cam_id = models.AutoField(primary_key=True)
    cam_location = models.CharField(max_length = 30)
    cam_ip = models.CharField(max_length = 20, unique = True)
    is_used = models.BooleanField(default=False)

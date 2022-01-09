from django.contrib import admin
from .models import Cctv
from .models import Record
# Register your models here.

admin.site.register(Cctv)
admin.site.register(Record)

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserSet)
admin.site.register(Medical_Information)
admin.site.register(druginformation)
admin.site.register(Notification)
admin.site.register(Share)
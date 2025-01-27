from django.contrib import admin
from .models import Profile, RecyclingData, RecyclingCenter

# Register your models here.



admin.site.register(Profile)
admin.site.register(RecyclingData)
admin.site.register(RecyclingCenter)
from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Interest)
admin.site.register(Event)
admin.site.register(Vote)
admin.site.register(UserInterest)
admin.site.register(UserCheckIn)

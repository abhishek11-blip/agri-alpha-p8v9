from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(PassType)
admin.site.register(UserPass)
admin.site.register(Trip)
admin.site.register(TransportMode)

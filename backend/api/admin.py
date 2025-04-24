from django.contrib import admin
from .models import Bd, Bl, Wb, CrawlTime, PushTime

admin.site.register(Bd)
admin.site.register(Bl)
admin.site.register(Wb)
admin.site.register(CrawlTime)
admin.site.register(PushTime)    
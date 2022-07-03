from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin
# Register your models here.
admin.site.register(Services)
admin.site.register(Contact)
admin.site.register(ContactUs)
admin.site.register(About)
admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(UserProfile)
admin.site.register(Banner)

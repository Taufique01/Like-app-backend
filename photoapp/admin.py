from django.contrib import admin
from django.contrib.auth.models import User
from photoapp.models import Like,Contest,PhotoUpload,UserAdmin,ContestAdmin,Profile,PhotoUploadAdmin
# Register your models here.
admin.site.register(Like)
admin.site.register(Contest,ContestAdmin)
#admin.site.register(UserAdmin)
admin.site.register(PhotoUpload,PhotoUploadAdmin)
admin.site.register(Profile)

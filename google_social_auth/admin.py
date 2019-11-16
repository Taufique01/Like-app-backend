from django.contrib import admin
from google_social_auth.models import AccessToken,Application
admin.site.register(AccessToken)
admin.site.register(Application)

# Register your models here.

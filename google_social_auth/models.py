from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.
from datetime import timedelta


from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from django.utils import timezone

from .common import generate_client_id, generate_client_secret,UNICODE_ASCII_CHARACTER_SET,CLIENT_ID_CHARACTER_SET




class Application(models.Model):

    CLIENT_CONFIDENTIAL = "confidential"
    CLIENT_PUBLIC = "public"
    CLIENT_TYPES = (
        (CLIENT_CONFIDENTIAL, "Confidential"),
        (CLIENT_PUBLIC, "Public"),
    )

    GRANT_AUTHORIZATION_CODE = "authorization-code"
    GRANT_IMPLICIT = "implicit"
    GRANT_PASSWORD = "password"
    GRANT_CLIENT_CREDENTIALS = "client-credentials"
    GRANT_TYPES = (
        (GRANT_AUTHORIZATION_CODE, "Authorization code"),
        (GRANT_IMPLICIT, "Implicit"),
        (GRANT_PASSWORD,"Resource owner password-based"),
        (GRANT_CLIENT_CREDENTIALS, "Client credentials"),
    )

    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(
        max_length=100, unique=True, default=generate_client_id, db_index=True
    )
    user = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s",
        null=True, blank=True, on_delete=models.CASCADE
    )

    #redirect_uris = models.TextField(
     #   blank=True, help_text=_("Allowed URIs list, space separated"),
    #)
    client_type = models.CharField(max_length=32, choices=CLIENT_TYPES)
    authorization_grant_type = models.CharField(
        max_length=32, choices=GRANT_TYPES
    )
    client_secret = models.CharField(
        max_length=255, blank=True, default=generate_client_secret, db_index=True
    )
    name = models.CharField(max_length=255, blank=True)
    skip_authorization = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

   
    def __str__(self):
        return self.name or self.client_id

   



class AccessToken(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True,
        related_name="access_token"
    )

    token = models.CharField(max_length=255, unique=True, )
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, blank=True, null=True,
    )
    expires = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_valid(self):
       
        return not self.is_expired()

    def is_expired(self):
      
        if not self.expires:
            return True

        return timezone.now() >= self.expires

    def revoke(self):
        
        self.delete()



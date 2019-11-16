from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from datetime import timedelta


class Contest(models.Model):

      title = models.CharField(max_length=500)
      entry = models.IntegerField(default=0)
      prize = models.IntegerField(default=0)
      max_participant =  models.IntegerField(default=0)
      name = models.CharField(max_length=500)  
      start_date = models.DateTimeField(
            default=timezone.now)
      end_date = models.DateTimeField(
            blank=True, null=True)
      start_date_str = models.CharField(max_length=500,default='no')
      end_date_str = models.CharField(max_length=500,default='no')    
      def __str__(self):
         return self.title

# Create your models here.
class PhotoUpload(models.Model):
    user = models.ForeignKey(
        User,
        related_name='photo_upload',
        null=False, blank=False, on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        Contest,
        related_name='photo_upload',
        null=False, blank=False, on_delete=models.CASCADE
    )
   
    upload_date = models.DateTimeField(
            default=timezone.now)
    image = models.ImageField(_("Image"), upload_to = 'images/%Y/%m/%d', blank=False, null=False)

    def __str__(self):
      return user.get_full_name()+str(self.upload_date)

class Like(models.Model):
    user = models.ForeignKey(
        User,
        related_name='photo_like',
        null=False, blank=False, on_delete=models.CASCADE
    )
    photo = models.ForeignKey(
        PhotoUpload,
        related_name='photo_lke',
        null=False, blank=False, on_delete=models.CASCADE
    )



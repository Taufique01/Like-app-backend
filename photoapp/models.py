from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from datetime import timedelta
from django.db.models import Count
from django.db.models.aggregates import Max
class Profile(models.Model):
   user = models.OneToOneField(
        User,
        related_name='profile',
        null=False, blank=False, on_delete=models.CASCADE
       )
   avatar=models.CharField(max_length=500,default='not found')
   total_earning = models.IntegerField(default=0)
   withdrawn = models.IntegerField(default=0)
   def __str__(self):
      return self.user.email

   def refreshContestWon(self):
          contests=Contest.objects.filter(user=self.user,end_date__lt=timezone.now())
          winner=self.photo_upload.annotate(like_count=Count('photo_lke')).order_by('-like_count')[0]
          earning=0
          for contest in contests:
              if contest.get_winner.user==self.user:
                 earning=earning+contest.prize
          self.total_earning=earning
          self.save()
   def availabeEarning(self):
       return self.total_earning+self.withdrawn
       
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
      
      user = models.ManyToManyField(User, related_name = 'contest', through='PhotoUpload')   
      def __str__(self):
         return self.title
      def get_winner(self):
         if self.photo_upload.count()==0:
            return False
         winner=self.photo_upload.annotate(like_count=Count('photo_lke')).order_by('-like_count')[0]
         return winner

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
    image = models.ImageField(_("Image"), upload_to = 'images/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
      return self.user.email+' '

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

    def __str__(self):
      return self.user.email+' '+self.photo.contest.title


class PaytmHistory(models.Model):
    user = models.ForeignKey(User,related_name='user_payment', on_delete=models.CASCADE)
    photo_upload = models.ForeignKey(PhotoUpload, related_name='photo_upload_payment', on_delete=models.CASCADE)
    TXNID = models.CharField('TNX ID', max_length=70)
    BANKTXNID = models.CharField('BANK TXN ID', max_length=60, null=True, blank=True)
    ORDERID = models.CharField('ORDER ID', max_length=70)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=30)
    TXNTYPE=models.CharField('TNX TYPE', max_length=10, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=20, null=True, blank=True)
    RESPCODE = models.CharField('STATUS', max_length=20)
    RESPMSG = models.TextField('RESP MSG', max_length=600)
    BANKNAME = models.CharField('BANK NAME', max_length=600, null=True, blank=True)
    MID = models.CharField(max_length=40)
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=20, null=True, blank=True)
    REFUNDAMT = models.FloatField('RFUND AMOUNT',default=0)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    #CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    
    def __str__(self):
        return str(self.photo_upload.id)




class PhotoUpload_inline(admin.TabularInline):
    model = PhotoUpload
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines = (PhotoUpload_inline,)
class ContestAdmin(admin.ModelAdmin):
    #readonly_fields = ['winner']

    inlines = (PhotoUpload_inline,)
    list_display= ['title', 'entry', 'prize', 'start_date', 'end_date','winner',]

    def winner(self,contest):
       winner_photo=contest.get_winner()
       if not winner_photo:
          return 'No result yet.'

       return winner_photo.user.email+' likes: '+str(winner_photo.photo_lke.count())


class PhotoUploadAdmin(admin.ModelAdmin):
      list_display= ['contest', 'email', 'upload_date', 'image','likes' ]
      
      def email(self,photo):
          return photo.user.email
      def likes(self,photo):
          return photo.photo_lke.all().count()
          






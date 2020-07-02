from rest_framework import serializers
from django import forms
from photoapp.models import Like,Contest,PhotoUpload
from django.db.models import Count
from django.db.models.aggregates import Max

class ContestSerializer(serializers.ModelSerializer):
    start_date_str = serializers.SerializerMethodField('get_start_date_str')
    end_date_str = serializers.SerializerMethodField('get_end_date_str')
    
    class Meta:
        model = Contest
        fields = ("id","title" , "entry", "prize", "max_participant", "start_date_str","end_date_str")

    def get_start_date_str(self, contest):
        return str(contest.start_date)

    def get_end_date_str(self, contest):
        return str(contest.end_date)
   

class MyContestSerializer(serializers.ModelSerializer):
   
    image_url = serializers.SerializerMethodField('get_image_url')
    likes = serializers.SerializerMethodField('get_like_count')
    start_date = serializers.SerializerMethodField('get_start_date_str')
    end_date = serializers.SerializerMethodField('get_end_date_str')
    class Meta:
        model = Contest
        fields = ('id','image_url','title','start_date','end_date','likes')

    def get_image_url(self, contest):
        user = self.context.get('user')

        photoup=contest.photo_upload.get(user=user)
        if not photoup.image:
           return None;
        return photoup.image.url
    
    def get_like_count(self, contest):
        user = self.context.get('user')
        photoup=contest.photo_upload.get(user=user)
        return photoup.photo_lke.all().count()

    def get_start_date_str(self, contest):
        return str(contest.start_date)

    def get_end_date_str(self, contest):
        return str(contest.end_date)


class PhotoFeedSerializer(serializers.ModelSerializer):
   
    image_url = serializers.SerializerMethodField('get_image_url')
    likes = serializers.SerializerMethodField('get_like_count')
    isLiked = serializers.SerializerMethodField('get_is_liked')
    username=serializers.SerializerMethodField('get_user_name')
    avatarUrl = serializers.SerializerMethodField('get_avatar_url')
    class Meta:
        model = PhotoUpload
        fields = ('id','image_url','username','avatarUrl','isLiked','likes')
    def get_user_name(self, photoUpload):
        user =  photoUpload.user
        return user.get_full_name()
         
  
    def get_image_url(self, photoUpload):

        if not photoUpload.image:
           return None;
        return photoUpload.image.url
    
    def get_like_count(self, photoUpload):
       
    
        return photoUpload.photo_lke.all().count()

    def get_avatar_url(self, photoUpload):
        user =  photoUpload.user
        return user.profile.avatar

    def get_is_liked(self, photoUpload):
        user = self.context.get('user')
        try:
          photoUpload.photo_lke.get(user=user)
         
        except Like.DoesNotExist:
          return False
       
        return True


class ImageUploadForm(forms.Form):
    """Image upload form."""
    token= forms.CharField(required=True)
    contest_id=forms.CharField(required=True)
    image = forms.ImageField()

class PhotoWinnerSerializer(serializers.ModelSerializer):
   
    image_url = serializers.SerializerMethodField('get_image_url')
    likes = serializers.SerializerMethodField('get_like_count')

    email=serializers.SerializerMethodField('get_user_mail')

    class Meta:
        model = PhotoUpload
        fields = ('image_url','email','likes')
    def get_user_mail(self, photoUpload):
        user =  photoUpload.user
        return user.email
         
    def get_image_url(self, photoUpload):

        if not photoUpload.image:
           return None;
        return photoUpload.image.url
    
    def get_like_count(self, photoUpload):
       
    
        return photoUpload.photo_lke.all().count()

class ContestHistorySerializer(serializers.ModelSerializer):

    end_date_str = serializers.SerializerMethodField('get_end_date_str')
    winner=PhotoWinnerSerializer(source='get_winner')
    class Meta:
        model = Contest
        fields = ("id","title" ,"prize", "winner", "end_date_str")
   
       
    def get_start_date_str(self, contest):
        return str(contest.start_date)

    def get_end_date_str(self, contest):
        return str(contest.end_date)





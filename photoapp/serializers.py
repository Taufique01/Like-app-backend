from rest_framework import serializers

from photoapp.models import Like,Contest,PhotoUpload


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
        photoup=contest.photo_upload
        if not photoup.image:
           return None;
        return photoup.image.url
    
    def get_like_count(self, contest):

        photoup=contest.photo_upload
        return photoup.photo_lke.all().count()

    def get_start_date_str(self, contest):
        return str(contest.start_date)

    def get_end_date_str(self, contest):
        return str(contest.end_date)
   


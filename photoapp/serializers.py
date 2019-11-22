from rest_framework import serializers

from photoapp.models import Like,Contest,PhotoUpload


class ContestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contest
        fields = ("id","title" , "entry", "prize", "max_participant", "start_date_str","end_date_str")




class MyContestSerializer(serializers.ModelSerializer):
    contest=ContestSerializer()
    #image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = PhotoUpload
        fields = ("contest",)
    def get_image_url(self, obj):
        return obj.image.url


from rest_framework import serializers

from photoapp.models import Like,Contest,PhotoUpload


class ContestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contest
        fields = ("title" , "entry", "prize", "max_participant", "start_date_str","end_date_str")




from rest_framework import serializers
from media.models import Media, MediaStatusChoices

        
class MediaSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only= True)
    retry_count = serializers.IntegerField(read_only= True)
    
    def validate(self, data):
        if self.instance and self.instance.status == MediaStatusChoices.SUCCESS:
            raise serializers.ValidationError("media have already sent, can't modify")
        return data
    
    class Meta:
        model = Media
        fields= '__all__'
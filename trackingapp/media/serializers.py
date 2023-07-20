from rest_framework import serializers
from media.models import Media, MediaStatusChoices

        
class WriteMediaSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        if self.instance and self.instance.status == MediaStatusChoices.SUCCESS:
            raise serializers.ValidationError("media have already sent, can't modify")
        return data
    
    class Meta:
        model = Media
        fields = ['media_from', 'media_to', 'content', 'content_type', 'sending_method']
        
class ListMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Media 
        exclude = ['content']
        
class RetriveMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Media
        fields= '__all__'
    
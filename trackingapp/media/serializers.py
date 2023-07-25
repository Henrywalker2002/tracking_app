from rest_framework import serializers
from media.models import Media, MediaStatusChoices
from user.serializers import ReadSortUserSerializer

        
class WriteMediaSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        if self.instance and self.instance.status == MediaStatusChoices.SUCCESS:
            raise serializers.ValidationError("media have already sent, can't modify")
        return data
    
    class Meta:
        model = Media
        fields = ['media_from', 'media_to', 'content', 'content_type', 'sending_method']
        
class ReadMediaSummarySerializer(serializers.ModelSerializer):
    
    created_by = ReadSortUserSerializer(read_only= True)
    updated_by = ReadSortUserSerializer(read_only= True)
    
    class Meta:
        model = Media 
        exclude = ['content']
        
class ReadMediaDetailSerializer(ReadMediaSummarySerializer):
    
    class Meta:
        model = Media
        fields = '__all__'
    
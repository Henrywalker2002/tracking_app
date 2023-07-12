from rest_framework import serializers
from media.models import Media

class ReadMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Media
        fields = '__all__'
        
class WriteMediaSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only= True)
    retry_count = serializers.IntegerField(read_only= True)
    
    
    class Meta:
        model = Media
        fields= '__all__'
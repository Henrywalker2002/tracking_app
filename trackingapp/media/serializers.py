from rest_framework import serializers
from media.models import Media

class ReadMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Media
        fields = '__all__'
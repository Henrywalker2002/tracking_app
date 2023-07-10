from rest_framework import serializers
from time_tracking.models.subcriber import Subcriber


class SubcriberSerializer(serializers.ModelSerializer):
    
    email_user = serializers.CharField(read_only= True) 

    class Meta:
        model = Subcriber
        fields = '__all__'

    def validate(self, data):
        instance = self.Meta.model.objects.filter(
            time_tracking=data.get('time_tracking'), user=data.get('user'))
        if instance:
            raise serializers.ValidationError(
                f"user {data.get('user')} have already subcribed to time tracking {data.get('time_tracking')}")
        return data
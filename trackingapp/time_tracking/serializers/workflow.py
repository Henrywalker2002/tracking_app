from rest_framework import serializers
from time_tracking.models.workflow import Workflow, WorkflowStep, Condition

class WorkflowSerializer(serializers.ModelSerializer):

    email_updated_by = serializers.CharField(read_only= True)
    email_created_by = serializers.CharField(read_only= True)

    class Meta: 
        model = Workflow
        fields=  '__all__'
    
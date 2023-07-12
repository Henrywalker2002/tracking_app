from base.views import BulkActionBaseModelViewSet
from time_tracking.models.workflow import Workflow, WorkflowStep, Condition
from time_tracking.serializers.workflow import WorkflowSerializer

class WorkflowModelViewSet(BulkActionBaseModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = {"default" : WorkflowSerializer}
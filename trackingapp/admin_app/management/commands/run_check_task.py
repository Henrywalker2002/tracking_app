from django.core.management.base import BaseCommand
from time_tracking.execute import check_task_over_deadline


class Command(BaseCommand):
    help = "command to check task"
    
    def handle(self, *args, **kwargs):
        print(123)
        check_task_over_deadline()
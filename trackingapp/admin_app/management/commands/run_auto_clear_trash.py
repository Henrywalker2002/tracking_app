from django.core.management.base import BaseCommand
from admin_app.trash_cleaner import auto_run_clean


class Command(BaseCommand):
    help = "command to run clean"
    
    def handle(self, *args, **kwargs):
        auto_run_clean()
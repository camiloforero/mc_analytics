from django.core.management.base import BaseCommand, CommandError
from mc_analytics import loadingScripts

class Command(BaseCommand):
    help = "Reloads all local and national offices' stats in measures such as opens, applied, accepted, realized and completed experiencies"

    def handle(self, *args, **options):
        loadingScripts.load_world_performance()

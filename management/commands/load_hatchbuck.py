# coding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from mc_analytics import hatchbuckScripts

class Command(BaseCommand):
    help = "Reloads all local and national offices' stats in measures such as opens, applied, accepted, realized and completed experiencies"

    def handle(self, *args, **options):
        hatchbuckScripts.load_expa_interaction('registered')
        hatchbuckScripts.load_expa_interaction('contacted')

from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page

from django_cctv.models import MonitorPage
from django_cctv.utli import update_monitor_script


class Command(BaseCommand):
    help = 'Update every monitor script'

    def handle(self, *args, **options):
        monitor_page = Page.objects.live().type(MonitorPage)

        for monitor in monitor_page:
            update_monitor_script(monitor)

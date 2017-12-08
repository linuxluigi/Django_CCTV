from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page
from cctv.settings import PROJECT_ROOT
import os

from django_cctv.models import MonitorPage


class Command(BaseCommand):
    help = 'start every active monitor'

    def handle(self, *args, **options):
        monitor_page = Page.objects.live().type(MonitorPage)

        for monitor in monitor_page:
            # get monitor
            monitor_page = MonitorPage.objects.get(pk=monitor.pk)
            monitor.stream_key = monitor_page.stream_key

            # try to run monitor script
            service_file_path = '%s/service/%s-service.sh' % (PROJECT_ROOT, monitor.stream_key)
            command_start = "%s start" % service_file_path
            os.system(command_start)

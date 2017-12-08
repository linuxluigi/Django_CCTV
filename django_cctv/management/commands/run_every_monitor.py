from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page

import os

from django_cctv.models import MonitorPage

from cctv.settings import PROJECT_ROOT


class Command(BaseCommand):
    help = 'Run every published Monitor'

    def handle(self, *args, **options):
        monitor_page = Page.objects.live().type(MonitorPage)

        for monitor in monitor_page:
            # add stream_key to monitor_page
            monitor_page = MonitorPage.objects.get(pk=monitor.pk)
            monitor.stream_key = monitor_page.stream_key

            # try to start every published monitor process
            service_file_path = '%s/service/%s-service.sh' % (PROJECT_ROOT, monitor.stream_key)
            command_start = "%s start" % service_file_path
            os.system(command_start)

import re

from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import datetime

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.signals import page_published, page_unpublished

import os


class MonitorIndexPage(Page):
    """
    Index all Monitors from this subcategory
    """
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    api_fields = ['intro', 'feed_image']


MonitorIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
]


# Monitor page

class MonitorPage(Page):
    """
    Single Monitor (Cam / Stream) Page
    """
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    stream_key = models.CharField(max_length=255, validators=[alphanumeric], unique=True, blank=False)
    stream_source = models.TextField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    cam_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('stream_key'),
        index.SearchField('body'),
    ]

    api_fields = ['stream_key', 'stream_source', 'body', 'cam_image']

    def get_video_records(self):
        """
        List all video records witch contain stream_key in the filename
        :return:
        """

        video_records = []

        root_path = "/srv/nginx/stream/record/"
        if os.path.isdir(root_path):
            for file_name in os.listdir(root_path):
                if re.match(self.stream_key + '-(\d{2})-(\D{3})-(\d{2})-(\d{2})-(\d{2})\.flv$', file_name):
                    file_path = os.path.join(root_path, file_name)
                    file_create_time = os.path.getctime(file_path)

                    # get file size as MB
                    file_size_mb = os.path.getsize(file_path) / 1024 / 1024

                    video_records.append({
                        'filename': file_name,
                        'create_date_time': datetime.datetime.fromtimestamp(file_create_time),
                        'file_size': "%d MB" % file_size_mb
                    })

        # sort array
        video_records = sorted(video_records, key=lambda k: k['create_date_time'], reverse=True)

        return video_records


MonitorPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('stream_key', classname="full"),
    FieldPanel('stream_source', classname="full"),
    ImageChooserPanel('cam_image'),
    FieldPanel('body', classname="full"),
]


def update_monitor_service(sender, **kwargs):
    """
    For each publish update create new service & run files for the cron job.
    """
    instance = kwargs['instance']
    from django_cctv.utli import update_monitor_script
    update_monitor_script(instance)


def remove_monitor_service(sender, **kwargs):
    """
    Remove service & run script when unpublished a MonitorPage .
    """
    instance = kwargs['instance']
    from django_cctv.utli import remove_monitor_script
    remove_monitor_script(instance)


# Register listeners for MonitorPage published signal
page_published.connect(update_monitor_service, sender=MonitorPage)

# Register listeners for MonitorPage unpublished signal
page_unpublished.connect(remove_monitor_service, sender=MonitorPage)

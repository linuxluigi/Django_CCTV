from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index


# Monitor index page

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
    stream_key = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('stream_key'),
        index.SearchField('body'),
    ]

    api_fields = ['stream_key', 'body', ]


MonitorPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('stream_key', classname="full"),
    FieldPanel('body', classname="full"),
]

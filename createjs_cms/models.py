from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent

from .utils import JSONLD

Page.register_extensions(
        'feincms.module.extensions.changedate',
        'feincms.module.extensions.datepublisher',
        'feincms.module.extensions.seo',
        'feincms.module.extensions.translations',
        )

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ),
    })

Page.create_content_type(RichTextContent)

JSONLD.register_model(Page)

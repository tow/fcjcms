from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def vie_subject(obj):
    return "/{0}/{1}/".format(
            ContentType.objects.get_for_model(obj).pk,
            obj.pk
            )

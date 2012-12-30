from __future__ import absolute_import

import json, re

from django.contrib.contenttypes.models import ContentType


class JSONLD(object):
    subject_re = re.compile('^</(?P<content_type>\d+)/(?P<object_id>.+)/>$')

    def __init__(self, d):
        if not d.get('@type') == "<http://www.w3.org/2002/07/owl#Thing>":
            raise ValueError("Not valid JSON-LD - no @type found")
        subject = d.get("@subject")
        if not subject:
            raise ValueError("Not valid JSON-LD - no @subject found")
        m = self.subject_re.match(subject)
        if not m:
            raise ValueError("Couldn't understand @subject")
        md = m.groupdict()
        self.object = ContentType.objects.get_for_id(md['content_type']).get_object_for_this_type(pk=md['object_id'])

    @classmethod
    def from_json(cls, body):
        try:
            d = json.loads(body)
        except ValueError:
            raise ValueError("Syntactically invalid JSON")
        if not isinstance(d, dict):
            raise ValueError("Not valid JSON-LD - not a dict")
        return cls(d)

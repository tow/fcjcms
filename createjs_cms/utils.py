from __future__ import absolute_import

import collections, json, re

from django.contrib.contenttypes.models import ContentType
from django.db import transaction


class JSONLD(object):
    subject_re = re.compile('^</(?P<content_type>\d+)/(?P<object_id>.+)/>$')
    rdfa_re = re.compile('^<http://viejs.org/ns/(?P<property>.*)>$')
    content_re = re.compile('^content-(?P<section>[A-Za-z]\w*)-(?P<oid>\d+)')

    registered_content_types = set()

    def __init__(self, d):
        self.rdfa = d.copy()

        if not self.rdfa.get('@type') == "<http://www.w3.org/2002/07/owl#Thing>":
            raise ValueError("Not valid JSON-LD - no @type found")
        del self.rdfa['@type']

        subject = self.rdfa.get("@subject")
        if not subject:
            raise ValueError("Not valid JSON-LD - no @subject found")
        del self.rdfa['@subject']

        m = self.subject_re.match(subject)
        if not m:
            raise ValueError("Couldn't understand @subject")
        md = m.groupdict()
        content_type = ContentType.objects.get_for_id(md['content_type'])
        if content_type not in self.registered_content_types:
            raise ValueError("This contenttype not available through JSONLD")
        self.object = content_type.get_object_for_this_type(pk=md['object_id'])

    @staticmethod
    def rdfa_property(property):
        return "<http://viejs.org/ns/{0}".format(property)

    @classmethod
    def from_json(cls, body):
        try:
            d = json.loads(body)
        except ValueError:
            raise ValueError("Syntactically invalid JSON")
        if not isinstance(d, dict):
            raise ValueError("Not valid JSON-LD - not a dict")
        return cls(d)

    @classmethod
    def register_model(cls, model):
        cls.registered_content_types.add(ContentType.objects.get_for_model(model))

    @transaction.commit_on_success()
    def update_model(self, save=False):
        attributes = RDFAttributes.from_rdfa(self.rdfa)
        content = attributes.pop('content')
        for section, l in content.items():
            s = getattr(self.object.content, section)
            assert len(l) == len(s)
            # should have done earlier checks to prevent us getting this far
            for (i, c) in enumerate(l):
                cm = s[i] # one contentmodel instance
                cm.text = c
                if save:
                    cm.save()
        for k, v in attributes.items():
            setattr(self.object, k, v)
        if save:
            self.object.save()

    def save(self):
        self.update_model(save=True)


class RDFAttributes(dict):
    @classmethod
    def from_rdfa(cls, rdfa):
        attributes = { "content": collections.defaultdict(dict) }
        for (k, v) in rdfa.items():
            m = JSONLD.rdfa_re.match(k)
            if not m:
                raise ValueError("Could not understand rdfa: {0}".format(k))
            property = m.groupdict()["property"]
            if property.startswith('content'):
                m = JSONLD.content_re.match(property)
                if not m:
                    raise ValueError("Could not understand content id: {0}".format(m))
                md = m.groupdict()
                attributes['content'][md['section']][int(md['oid'])] = v
            else:
                attributes[property] = v
        # sanity check content section, plus turn dicts into lists
        for (section, d) in attributes['content'].items():
            if sorted(d.keys()) != list(range(len(d))):
                print(sorted(d.keys()))
                print(list(range(len(d))))
                raise ValueError("Some content missing from rdfa content: {0}".format(section))
            attributes['content'][section] = [v for (k, v) in sorted(d.items())]
        return cls(**attributes)

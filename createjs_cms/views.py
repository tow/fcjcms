from __future__ import absolute_import

import json

from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseBadRequest

from .utils import JSONLD


class PageUpdateView(View):
    def put(self, request, *args, **kwargs):
        try:
            json_ld = JSONLD.from_json(request.body.decode('utf8'))
        except ValueError:
            return HttpResponseBadRequest()
        object = json_ld.object
        print(json_ld, json_ld.object, json_ld.rdfa)
        print(json_ld.attributes_from_rdfa())
        return HttpResponse(status=204)

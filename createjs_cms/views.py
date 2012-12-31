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
        json_ld.save()
        return HttpResponse(status=204)

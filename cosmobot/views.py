import copy, json, datetime

from djano.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import WebhookTransaction


@csrf_exempt
@require_POST
def webook(request):
    jsondata = request.body
    data = json.loads(jsondata)
    meta = copy.copy(request.META)
    for k, v in meta.items():
        if not isinstance(v, basestring):
            del meta[k]

    WebhookTransaction.objects.create(
        date_event_generated=datetime.datetime.fromtimestamp(
            data['timestamp']/1000.0,
            tz=timezone.get_current_timezone()
        ),
        body=data,
        request_meta=meta
    )

    return HttpResponse(status=200)


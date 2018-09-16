from django.db import models
from django.utils import timezone

from django_hstore import hstore


class WebhookTransaction(models.Model):
    UNPROCESSED = 1
    PROCESSED = 2
    ERROR = 3

    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    date_generated = models.DateTimeField()
    date_received = models.DateTimeField(default=timezone.now)
    body = hstore.SerializedDictionaryField()
    request_data = hstore.SerializedDictionaryField()
    status = model.CharField(max_length=250, choices=STATUSES, default=UNPROCESSED)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return u'{0}'.format(self.date_event_generated)


class Message(models.Model):
    date_processed = models.DateTimeField(default=timezone.now)
    webhook_transaction = models.OneToOneField(WebhookTransaction)
    
    chat_id = models.IntegerField(unique=True)
    chat_text = models.CharField()

    def __unicode__(self):
        return u'{}'.format(self.chat_id)

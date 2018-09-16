from celery.task import PeriodicTask
from celery.schedules import crontab

from .models import Message, WebhookTransaction


class ProcessMessages(PeriodicTask):
    run_every = crontab()

    def run(self, **kwargs):
        unprocessed_transactions = self.get_unprocessed_transactions()

        for transaction in unprocessed_transactions:
            try:
                self.process(transaction)
                transaction.status = WebhookTransaction.PROCESSED

            except Exception:
                transaction.status = WebhookTransaction.ERROR

            finally:
                transaction.save()


    def get_unprocessed_transactions(self):
        return WebhookTransaction.objects.filter(
            event_name__in=self.event_names,
            status=WebhookTransaction.UNPROCESSED
        )


    def process(self, transaction):
        return Message.objects.create(
            chat_id=transaction.body['id']
            chat_text=transaction.body['text']
            webhook_transaction=transaction
        )

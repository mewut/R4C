from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = "customers"

    def ready(self):
        from .signals import send_notification_email
        from django.db.models.signals import post_save
        from .models import Customer

        post_save.connect(send_notification_email, sender=Customer)
        
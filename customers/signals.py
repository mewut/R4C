import django
from django.apps import apps
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=apps.get_model('customers', 'Customer'))
def send_notification_email(sender, instance, created, **kwargs):
    django.setup()
    from .models import Customer 
    Robot = apps.get_model('robots', 'Robot')
    if Robot.objects.filter(quantity__gt=0).exists():
        robot = instance.robot
        subject = 'Робот в наличии'
        message = f'Добрый день!\nНедавно вы интересовались нашим роботом модели {robot.model}, версии {robot.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'
        from_email = 'noreply@example.com'
        recipient_list = ['user@example.com']
        send_mail(subject, message, from_email, recipient_list)

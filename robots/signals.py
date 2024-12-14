from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Robot
from orders.models import Order
from django.conf import settings

@receiver(post_save, sender=Robot)
def send_robot_in_stock_notification(sender, instance, created, **kwargs):
    if not created and instance.in_stock:
        orders = Order.objects.filter(robot_serial=instance.serial)

        for order in orders:
            customer = order.customer 
            subject = f"Робот модели {instance.model}, версии {instance.version} теперь в наличии!"
            message = f"""
            Добрый день!
            Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.
            """

            send_mail(
                subject, 
                message, 
                settings.DEFAULT_FROM_EMAIL, 
                [customer.email], 
                fail_silently=False,
            )


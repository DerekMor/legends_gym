from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Customer
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model


@receiver(user_signed_up)
def create_customer_for_new_user(sender, request, user, **kwargs):
    # Create a Customer record associated with the new user
    print("Creating customer for new user:", user)
    customer = Customer.objects.create(user=user)
    # Mark the user's email as verified
    email_address = EmailAddress.objects.get(user=user, primary=True)
    email_address.verified = True
    email_address.save()

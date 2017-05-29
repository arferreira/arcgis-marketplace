from django.conf import settings
from django.dispatch import receiver

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received


@receiver(valid_ipn_received)
def paypal_ipn_invoice(sender, **kwargs):
    paypal_ipn = sender

    if (paypal_ipn.payment_status == ST_PP_COMPLETED and
            paypal_ipn.receiver_email == settings.PAYPAL_BUSINESS):

        # check the amount received etc. are all what you expect.
        # Undertake some action depending upon `paypal_ipn`.
        if paypal_ipn.custom == 'hi!':
            pass

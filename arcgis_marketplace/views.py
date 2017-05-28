import uuid

from django.conf import settings
from django.urls import reverse
from django.views.generic import DetailView

from paypal.standard.forms import PayPalPaymentsForm

from . import models


class ItemPaypalFormView(DetailView):
    model = models.Item
    template_name = 'arcgis_marketplace/paypal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        _build_uri = self.request.build_absolute_uri
        context['form'] = PayPalPaymentsForm(initial={
            'business': settings.PAYPAL_BUSINESS,
            'amount': "{:.2f}".format(self.object.price),
            'item_name': self.object.title,
            'invoice': uuid.uuid4().hex,
            'notify_url': _build_uri(reverse('paypal-ipn')),
            'return_url': _build_uri('paypal-success'),
            'cancel_return': _build_uri('paypal-cancel'),
            'currency_code': 'EUR'
        })

        return context

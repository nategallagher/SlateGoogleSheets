#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Efforia Open Source Initiative.
#
# Copyright (C) 2011-2014 William Oliveira de Lagos <william@efforia.com.br>
#
# Shipping is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shipping is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Shipping. If not, see <http://www.gnu.org/licenses/>.
#

from django.utils.translation import ugettext as _

try:
    from mezzanine.conf import settings
    from cartridge.shop.utils import set_shipping
    from cartridge.shop.models import Cart
    from cartridge.shop.forms import OrderForm
except ImportError,e:
    pass

from shipping.codes import CorreiosCode
from shipping.fretefacil import FreteFacilShippingService
from shipping.models import DeliverableProperty

def fretefacil_shipping_handler(request, form, order=None):
    if request.session.get("free_shipping"): return
    settings.use_editable()
    if form is not None: user_postcode = form.cleaned_data['shipping_detail_postcode']
    else: user_postcode = settings.STORE_POSTCODE 
    user_postcode = form.cleaned_data['shipping_detail_postcode']
    shippingservice = FreteFacilShippingService()
    cart = Cart.objects.from_request(request)
    delivery_value = 0.0
    if cart.has_items():
        for product in cart:
            properties = DeliverableProperty.objects.filter(sku=product.sku)
            if len(properties) > 0:
                props = properties[0]
                deliverable = shippingservice.create_deliverable(settings.STORE_POSTCODE,
                                                                 user_postcode,
                                                                 props.width,
                                                                 props.height,
                                                                 props.length,
                                                                 props.weight)
                delivery_value += float(shippingservice.delivery_value(deliverable))
    set_shipping(request, _("Correios"),delivery_value)

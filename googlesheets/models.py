from django.db import models
from geo.models import Address
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import encoding

import pickle
import base64
import oauth2client


from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_orm import CredentialsField


class Shipment(models.Model):
    address = models.ForeignKey(Address, verbose_name=_("Address"), null=True, blank=True)
    ship_date = models.DateTimeField("Date Shipped", blank=True, null=True)


class ShipmentAdmin(admin.ModelAdmin):
    pass


class CredentialsModel(models.Model):
	id = models.ForeignKey(User, primary_key=True)
	#user = models.OneToOneField(User)
  	credential = CredentialsField()

class CredentialsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CredentialsModel, CredentialsAdmin)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^oauth2client\.contrib\.django_orm\.CredentialsField"])

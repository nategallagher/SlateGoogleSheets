from googlesheets.models import Shipment
from django.contrib import admin

class ShipmentAdmin(admin.ModelAdmin):
    """
    Administrator interface of Shipment model.
    """
    list_display  = ('address', 'ship_date', )
admin.site.register(Shipment, ShipmentAdmin)
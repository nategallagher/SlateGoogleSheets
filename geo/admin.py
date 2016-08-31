from django.contrib import admin
from geo.models import Address, State, City, Country

class AddressAdmin(admin.ModelAdmin):
    """
    Administrator interface of Address model.
    """
    list_display  = ('street', 'city', 'postal_code', )
admin.site.register(Address, AddressAdmin)

class StateAdmin(admin.ModelAdmin):
    """
    Administrator interface of State model.
    """
    list_display  = ('name', 'abbr', 'country', )
admin.site.register(State, StateAdmin)

class CityAdmin(admin.ModelAdmin):
    """
    Administrator interface of City model.
    """
    list_display  = ('name',)
    list_filter = ('state__name',)
admin.site.register(City, CityAdmin)

admin.site.register(Country)

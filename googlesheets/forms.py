from django import forms
from django.forms import ModelForm
from googlesheets.models import Shipment
from geo.models import Address, City, WalzState, State
from geo.forms import CityField
from googlesheets.widgets import DateInputWithDatepicker
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList
import string
import logging
log = logging.getLogger(__name__)

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class ShipmentForm(ModelForm):
    # in model
    street_address = forms.CharField(label=_("Street Address"), required=False)
    city = forms.CharField(label=_("City"), required=False)
    state = forms.ModelChoiceField( queryset=State.objects.all(), 
                                    to_field_name="abbr", 
                                    label=_("State"), 
                                    required=False, 
                                  )
    zip = forms.CharField(label=_("Zip Code"), required=False)
    #ship_date = forms.DateField(label=_("Shipment Date"), widget=DateInputWithDatepicker, required=False)
    ship_date = forms.DateField(label=_("Shipment Date"), widget=DateInput(), required=False)

    # not in model yet
    order_date = forms.DateField(label=_("Date of Order"), widget=DateInput(), required=False)
    dealer_name = forms.CharField(label=_("Dealer Name"), required=False)
    customer_name = forms.CharField(label=_("Customer Name"), required=False)
    country = forms.CharField(label=_("Country"), required=False)
    customer_phone = forms.CharField(label=_("Customer Phone"), required=False)
    customer_email = forms.EmailField(label=_("Customer Email"), required=False)
    sku_number = forms.CharField(label=_("SKU"), required=False)
    MODEL_TYPE_CHOICES = [['', '---------'], ['MTi2', 'MTi2']]
    model_type = forms.ChoiceField(label=_("Model"), choices=MODEL_TYPE_CHOICES, required=False)
    ITEM_CONDITION_CHOICES = [['', '---------'], ['A Stock', 'A Stock'], ['B Stock', 'B Stock'], ['Refurbished', 'Refurbished'], ['Demo', 'Demo']]
    item_condition = forms.ChoiceField(label=_("Item Condition"), choices=ITEM_CONDITION_CHOICES, required=False)
    unit_number = forms.CharField(label=_("Number of Units"), required=False)
    order_number = forms.CharField(label=_("Order Number"), required=False)
    po_number = forms.CharField(label=_("PO #"), required=False)
    slate_invoice_number = forms.CharField(label=_("Slate Invoice #"), required=False)
    PRIORITY_CHOICES = [['', '---------'], ['1', '1 = Sweat'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10 = No Sweat']]
    priority = forms.ChoiceField(label=_("Priority"), choices=PRIORITY_CHOICES, required=False)
    order_notes = forms.CharField(label=_("Notes"), widget=forms.Textarea, required=False)
    promised_date = forms.DateField(label=_("Is there a promised date?"), widget=DateInput(), required=False)
    ship_number = forms.CharField(label=_("Ship Number - Sales"), required=False)
    billing_address = forms.CharField(label=_("Billing Address"), required=False)
    addtl_ship_info = forms.CharField(label=_("Add additional shipping info if you like."), widget=forms.Textarea, required=False)
    addtl_notes = forms.CharField(label=_("Additional Notes"), widget=forms.Textarea, required=False)
    warranty_date = forms.DateField(label=_("Warranty Exp Date"), widget=DateInput(), required=False)


    class Meta:
        model = Shipment

    def __init__(self, *args, **kwargs):
        super(ShipmentForm, self).__init__(*args, **kwargs)

    def fieldtest(self, cd, nonfieldlist, fielderror, fieldname, nonfielderror):
        value = cd.get(fieldname)
        if (not value and value != 0) or str(value).isspace():
            if not self._errors.has_key(fieldname):
                self._errors[fieldname] = ErrorList()
            self._errors[fieldname].append(fielderror)
            nonfieldlist.append(nonfielderror)
        return nonfieldlist

    def clean(self):
        cd = super(ShipmentForm, self).clean()

        missing_reqs = []
        fielderror = "Required."
        # check for Street Address field and correct capitalization if present
        street_address_string = cd.get('street_address')
        if (not street_address_string and street_address_string != 0) or str(street_address_string).isspace():
            if not self._errors.has_key('street_address'):
                self._errors['street_address'] = ErrorList()
            self._errors['street_address'].append(fielderror)
            missing_reqs.append('Street Address')
        else:
            cd['street_address'] = string.capwords(street_address_string)
        # check for City field and correct capitalization if present
        city_string = cd.get('city')
        if (not city_string and city_string != 0) or str(city_string).isspace():
            if not self._errors.has_key('city'):
                self._errors['city'] = ErrorList()
            self._errors['city'].append(fielderror)
            missing_reqs.append('City')
        else:
            cd['city'] = string.capwords(city_string)
        #missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'state', 'State')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'zip', 'Zip Code')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'ship_date', 'Shipment Date')

        # required not in model yet
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'dealer_name', 'Dealer Name')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'model_type', 'Model')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'item_condition', 'Item Condition')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'unit_number', 'Number of Units')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'order_number', 'Order Number')
        missing_reqs = self.fieldtest(cd, missing_reqs, fielderror, 'priority', 'Priority')

        #stringify python objects
        #cd['ship_date'] = str(cd.get('ship_date'))
        ##cd['order_date'] = str(cd.get('order_date'))
        #cd['promised_date'] = str(cd.get('promised_date'))
        #cd['warranty_date'] = str(cd.get('warranty_date'))
        #cd['state'] = str(cd.get('state'))



        # debug printout of corrected values
        data_list = [
            'street_address', 
            'city',
            'state',
            'zip',
            'ship_date'
        ]
        for key, value in cd.iteritems():
            try:
                i = data_list.index(key)
            except:
                i = 0
            debug_value = 'forms.ShipmentForm: %03d. %s => %s' % (i, key, value)
            log.debug(debug_value)

        # print missing required fields at top of form
        if len(missing_reqs) > 0:
            all_errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
            error_heading = "PLEASE FILL-IN THE FOLLOWING REQUIRED FIELDS:"
            if error_heading not in all_errors:
                all_errors.append(error_heading)
            log.debug(all_errors)
            for req_field in missing_reqs:
                all_errors.append(req_field)

        return cd

    '''
    def is_valid(self):        
        is_valid = super(ShipmentForm, self).is_valid()
        log.debug('ShipmentForm: is_valid => %s',is_valid)
        return is_valid
    '''

    def save(self, commit=True):
        state_obj = State.objects.get(name=self.cleaned_data['state'])
        city_obj, created = City.objects.get_or_create(name=self.cleaned_data['city'], state=state_obj)
        city_obj.save()
        address_obj, created = Address.objects.get_or_create(
            street=self.cleaned_data['street_address'],
            city=city_obj,
            postal_code=self.cleaned_data['zip']
        )
        address_obj.save()
        shipment, created = Shipment.objects.get_or_create(
            address=address_obj,
            ship_date=self.cleaned_data['ship_date']
        )
        shipment.save()
        #return super(ShipmentForm, self).save()
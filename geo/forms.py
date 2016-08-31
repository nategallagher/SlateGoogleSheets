from django import forms
from django.utils.translation import ugettext as _
from django.forms.util import ValidationError

from geo.models import City, State, Address

import logging
log = logging.getLogger(__name__)


class CityField(forms.ModelChoiceField):
    def clean(self, value):
        #forms.Field.clean(self, value)
        #if self.required and value in (None, ''):
        #    raise ValidationError(self.error_messages['required'])
        #return self.to_python(value)
        return value

    def to_python(self, value):
        if value in (None, '', [], (), {}):
            return None
        key = self.to_field_name or 'pk'
        if key == 'name':
            value = self.queryset.filter(name__iexact='%s' % value)
        else:
            value = self.queryset.filter(**{key: value})
        if value.count() > 0:
            value = value[0]
        else:
            #if no city could be located, return.
            #presumably it will be created later on on the form
            return None
        return value

class BaseAddressForm(forms.ModelForm):
    street = forms.CharField(label=_("Street"), max_length=255)
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=True)
    city = CityField(queryset=City.objects.all(), to_field_name="name", required=True,
                    )
    postal_code = forms.CharField(label=_("Zip"), required=True)

    def __init__(self, *args, **kwargs):
        prefix = kwargs.get("prefix")
        super(BaseAddressForm, self).__init__(*args, **kwargs)
        if prefix:
            self.fields["city"].widget.set_prefix_suffix(prefix)
        instance = kwargs.get("instance", None)
        if not instance is None and instance.city:
            self.initial['city'] = instance.city
            self.initial['state'] = instance.city.state.id

    def clean_city(self, *args, **kwargs):
        city = None
        state = self.cleaned_data.get('state', None)
        city_name = self.cleaned_data.get('city', None)
        if city_name:
            if all([city_name.strip(), state]):
                city, created = City.objects.get_or_create(name=city_name, state=state)
        if not city and self.fields['city'].required:
            raise ValidationError('The City field is required')
        return city

        #if self.prefix and all([self.fields["state"].required, self.fields["city"].required]):
        #    if state and not cd.get('city') and self.data.has_key(self.prefix+'-city'):
        #        city_name = self.data.get(self.prefix+ '-city')
        #        if city_name.strip():
        #            city, created = City.objects.get_or_create(name=city_name, state=state)
        #            cd['city']= city
        #            if created:
        #                log.debug('created city %s' % city.name)
        #log.debug(cd)
        #log.debug('done with clean city--'*10)

    #def clean(self, *args, **kwargs):
    #    log.debug('cleaning...')
    #    log.debug(">>>>> "+self.prefix)
    #    super(BaseAddressForm, self).clean(*args, **kwargs)
    #    cd = self.cleaned_data
    #    log.debug(cd)
    #    return cd

    #def is_valid(self):
    #    super(BaseAddressForm, self).is_valid()

    class Meta:
        model = Address
        fields = ('street', 'state', 'city', 'postal_code')


class AddressNotRequiredForm(BaseAddressForm):
    def __init__(self, *args, **kwargs):
        super(AddressNotRequiredForm, self).__init__(*args, **kwargs)
        self.fields["street"].required = False
        self.fields["state"].required = False
        self.fields["city"].required = False
        self.fields["postal_code"].required = False


    def clean(self):
        cd = self.cleaned_data
        super(AddressNotRequiredForm, self).clean()
        log.debug('cleaning not-required-address with data: %s' % str(cd))
        #if cd.get('state') and not cd.get('city'):
        #    raise ValidationError('When selecting a state, please choose a city.')
        return cd


    def save(self, commit=True):
        if any(self.cleaned_data.values()):
            address = super(AddressNotRequiredForm, self).save(commit=False)
            address.save()
            return address

from django.db import models
from django.utils.translation import ugettext as _


class Country(models.Model):
    """
    Country list
    """
    USA_PK = 1
    CANADA_PK = 2
    NORTH_AMERICA = (USA_PK, CANADA_PK, )

    name = models.CharField(_('Country name'), max_length=128, unique=True)
    active = models.BooleanField(_('Country is active'), default=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Country')
        verbose_name_plural = _(u'Countries')

class State(models.Model):
    """
    US state/Canada province
    """
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    name = models.CharField(_('State/Province name'), max_length=128)
    abbr = models.CharField(_('State/Province abbr'), max_length=4)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return u"%s" % self.name

class WalzState(State):
    class Meta:
        proxy = True

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.abbr)

class City(models.Model):
    """
    City
    """
    state = models.ForeignKey(State, verbose_name=_("State"))
    name = models.CharField(_('City name'), max_length=256)

    class Meta:
        unique_together = ('state', 'name')
        ordering = ['name']
        verbose_name = _('City')
        verbose_name_plural = _(u'Cities')

    def __unicode__(self):
        return u"%s" % (self.name, )

class Address(models.Model):
    """
    Addresses
    """
    street = models.CharField(_("Street"), max_length=1000,
                              null=True, blank=True)
    city = models.ForeignKey(City, verbose_name=_("City"),
                             null=True, blank=True)
    postal_code = models.CharField(_("Zip"), max_length=30,
                                   null=True, blank=True)

    def __unicode__(self):
        return u"%s, %s, %s %s" % (self.street, self.city, self.city.state.abbr, self.postal_code)

    class Meta:
        verbose_name = _(u'Address')
        verbose_name_plural = _(u'Addresses')

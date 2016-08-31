from tddspry.django.cases import DatabaseTestCase

from roa.geo.models import Country, State, City, Address


class TestCountry(DatabaseTestCase):
    """
    Test Country model
    """

    def test_create(self):
        self.assert_create(Country, name="Ukraine")

    def test_update(self):
        country = self.assert_create(Country, name="Ukraine")
        self.assert_update(country, active=True)
        
    def test_unicode(self):
        country = self.assert_create(Country, name="Ukraine")
        self.assert_equal(country.__unicode__(), "Ukraine")

class TestCity(DatabaseTestCase):
    """
    Test City and State model
    """

    def test_create(self):
        country = self.assert_create(Country, name="Ukraine")
        state = self.assert_create(State, country=country, name="Kyiv region")
        city = self.assert_create(City, state=state, name="Kyiv")

    def test_update(self):
        country = self.assert_create(Country, name="Ukraine")
        state = self.assert_create(State, country=country, name="Kyiv region")
        city = self.assert_create(City, state=state, name="Kyiv")
        self.assert_update(city, name="Irpin")
        self.assert_update(state, name="Crimea")
        

class TestAddress(DatabaseTestCase):
    """
    Test Address model
    """
    address_test = {"street": "Slinko"}

    def test_create(self):
        country = Country.objects.get(pk=1)
        city = City.objects.get(pk=2)
        self.address_test['city'] = city
        self.assert_create(Address, **self.address_test)

    def test_update(self):
        city = City.objects.get(pk=2)
        self.address_test['city'] = city
        address = self.assert_create(Address, **self.address_test)
        self.assert_update(address, street='Petra')
        self.assert_update(address, city=city)

    def test_unicode(self):
        city = City.objects.get(pk=1)
        self.address_test['city'] = city
        address = self.assert_create(Address, **self.address_test)
        unicode_test =  u"%s %s" % (self.address_test['street'], \
                                    self.address_test['city'], )
        self.assert_equal(address.__unicode__(), unicode_test)

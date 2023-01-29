import factory
import django
from blog.models import Partner

class PartnerFactory(factory.Factory):
    class Meta:
        model = Partner

    name = 'X Partner'

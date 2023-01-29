import factory
import django
from blog.models import Lender

class LenderFactory(factory.Factory):
    class Meta:
        model = Lender

    name = 'X Lender'
    interest_rate = 0.05
    points = 0.2

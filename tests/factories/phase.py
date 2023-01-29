import factory
import django
from blog.models import Phase, Owner, Plat
from tests.factories.owner import OwnerFactory
from tests.factories.plat import PlatFactory

class PhaseFactory(factory.Factory):
	class Meta:
		model = Phase

	number = 10
	plat = PlatFactory(name='phase plat')
	owner = OwnerFactory()
	# name = 'phase plat :PH 10'
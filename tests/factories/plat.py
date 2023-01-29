import factory
import django
from blog.models import Plat
from tests.factories.community import CommunityFactory
from tests.factories.partner import PartnerFactory

class PlatFactory(factory.Factory):
	class Meta:
		model = Plat

	partner = PartnerFactory()
	name = "This is a plat"
	date_posted = None
	community = CommunityFactory()
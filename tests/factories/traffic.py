import factory
import django
from blog.models import Traffic, Plat
from tests.factories.plat import PlatFactory

class TrafficFactory(factory.Factory):
	class Meta:
		model = Traffic

	plat = PlatFactory()
	count = 123
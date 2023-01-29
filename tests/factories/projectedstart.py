import factory
import django
from blog.models import ProjectedStart
from tests.factories.plat import PlatFactory

class ProjectedStartFactory(factory.Factory):
	class Meta:
		model = ProjectedStart

	plat = PlatFactory()
	count = 5
	source = "naturally"
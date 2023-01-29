import factory
import django
from blog.models import Goal
from tests.factories.plat import PlatFactory

class GoalFactory(factory.Factory):
	class Meta:
		model = Goal

	plat = PlatFactory()
	count = 5
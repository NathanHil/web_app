import factory
import django
from blog.models import Job
from tests.factories.phase import PhaseFactory
from tests.factories.plan import PlanFactory

class JobFactory(factory.Factory):
	class Meta:
		model = Job

	number = '000-00-000'
	phase = PhaseFactory()
	lot_number = 420
	sales_status = ''
	plan = PlanFactory()
	sales_price = 100000.00
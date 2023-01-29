import factory
import django
from blog.models import Investor

class InvestorFactory(factory.Factory):
	class Meta:
		model = Investor

	name = 'X Investor'
	total_capacity = 69
import factory
import django
from blog.models import CostCode

class CostCodeFactory(factory.Factory):
	class Meta:
		model = CostCode

	number = 'X CostCode'
	description = 'This is a cost code'
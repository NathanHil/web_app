import factory
import django
from blog.models import LoanTransaction
from tests.factories.cost_code import CostCodeFactory
#from tests.factories.master_plan import MasterPlanFactory

class LoanTransactionFactory(factory.Factory):
	class Meta:
		model = LoanTransaction

	costcode = CostCodeFactory()
	# Master plan not implimented yet
	#masterplan = MasterPlanFactory()
	amount = 200000.00
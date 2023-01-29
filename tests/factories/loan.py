import factory
import django
from blog.models import Loan
from tests.factories.job import JobFactory
from tests.factories.lender import LenderFactory

class LoanFactory(factory.Factory):
    class Meta:
        model = Loan

    job = JobFactory()
    lender = LenderFactory()
    number = 5
    receive_cash_back = False
    note = "hello world"
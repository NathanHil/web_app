from django.test import TestCase
from tests.factories.loan import LoanFactory
from tests.factories.job import JobFactory
from tests.factories.lender import LenderFactory

class LoanModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Loan = LoanFactory._meta.model
    def test_crud_loan(self):
        # CREATE
        loan = LoanFactory(number=10)

        # READ
        self.assertEqual(loan.number, 10)
        self.assertEqual(loan.job.number, '000-00-000')
        self.assertEqual(loan.lender.name, 'X Lender')
        self.assertEqual(loan.receive_cash_back, False)
        self.assertEqual(loan.note, "hello world")
        
        # UPDATE
        loan.number = 5
        loan.job.number = '123-45-678'
        self.assertEqual(loan.number, 5)
        self.assertEqual(loan.job.number, '123-45-678')
        self.assertIsNot(loan.lender.name, 'Y Lender')
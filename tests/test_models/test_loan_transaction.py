from django.test import TestCase
from tests.factories.loan_transaction import LoanTransactionFactory
from tests.factories.cost_code import CostCodeFactory

class LoanTransactionModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.CostCode = CostCodeFactory._meta.model
    def test_crud_loan_transaction(self):

        # CREATE (default)
        LT = LoanTransactionFactory()

        # READ
        self.assertEqual(LT.costcode.number, 'X CostCode')
        self.assertEqual(LT.amount, 200000.00)
        self.assertEqual(LT.pk, LT.id)

        # UPDATE
        LT.costcode.number = 'Y CostCode'
        LT.amount = 100000.00
        self.assertEqual(LT.costcode.number, 'Y CostCode')
        self.assertEqual(LT.amount, 100000.00)
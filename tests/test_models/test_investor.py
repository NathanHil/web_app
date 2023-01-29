from django.test import TestCase
from tests.factories.investor import InvestorFactory

class InvestorModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Investor = InvestorFactory._meta.model
    def test_crud_investor(self):

        # CREATE (default)
        investor = InvestorFactory()

        # READ
        self.assertEqual(investor.name, 'X Investor')
        self.assertEqual(investor.total_capacity, 69)
        self.assertEqual(investor.pk, investor.id)

        # UPDATE
        investor.name = 'Y Investor'
        investor.total_capacity = 42
        self.assertEqual(investor.name, 'Y Investor')
        self.assertEqual(investor.total_capacity, 42)
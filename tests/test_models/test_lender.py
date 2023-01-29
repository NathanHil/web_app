from django.test import TestCase
from tests.factories.lender import LenderFactory

class LenderModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Lender = LenderFactory._meta.model
    def test_crud_lender(self):
        # CREATE
        lender = LenderFactory(name='X Lender')

        # READ
        self.assertEqual(lender.name, 'X Lender')
        self.assertEqual(lender.interest_rate, 0.05)
        self.assertEqual(lender.points, 0.2)
        self.assertEqual(lender.ltc_limit, 0)
        self.assertEqual(lender.ltv_limit, 0)
        self.assertEqual(lender.pk, lender.id)
        
        # UPDATE
        lender.name = 'Y Lender'
        lender.interest_rate = 0.02
        self.assertEqual(lender.name, 'Y Lender')
        self.assertEqual(lender.interest_rate, 0.02)
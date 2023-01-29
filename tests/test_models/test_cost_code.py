from django.test import TestCase
from tests.factories.cost_code import CostCodeFactory

class CostCodeModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.CostCode = CostCodeFactory._meta.model
    def test_crud_cost_code(self):

        # CREATE (default)
        cost_code = CostCodeFactory()

        # READ
        self.assertEqual(cost_code.number, 'X CostCode')
        self.assertEqual(cost_code.is_hard, True)
        self.assertEqual(cost_code.description, 'This is a cost code')
        self.assertEqual(cost_code.pk, cost_code.id)

        # UPDATE
        cost_code.number = 'Y CostCode'
        cost_code.is_hard = False
        cost_code.description = 'This is also a cost code'
        self.assertEqual(cost_code.number, 'Y CostCode')
        self.assertEqual(cost_code.is_hard, False)
        self.assertEqual(cost_code.description, 'This is also a cost code')
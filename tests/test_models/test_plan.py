from django.test import TestCase
from tests.factories.plan import PlanFactory

class PlanModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Plan = PlanFactory._meta.model
    def test_crud_plan(self):
        # CREATE
        plan = PlanFactory()

        # READ (default)
        self.assertEqual(plan.name, 'X Plan')
        self.assertEqual(plan.last_updated, None)
        self.assertEqual(plan.size, 100)
        self.assertEqual(plan.garage_count, 1)
        self.assertEqual(plan.stories, 2)
        self.assertEqual(plan.bedroom_count, 0)
        self.assertEqual(plan.bath_count, 0)
        self.assertEqual(plan.width, 0)
        self.assertFalse(plan.is_active)
        self.assertFalse(plan.is_attached)
        self.assertEqual(plan.pk, plan.id)
        
        # UPDATE
        plan.name = 'Y Plan'
        plan.bedroom_count = 5
        plan.is_active = True
        self.assertEqual(plan.name, 'Y Plan')
        self.assertEqual(plan.bedroom_count, 5)
        self.assertTrue(plan.is_active)

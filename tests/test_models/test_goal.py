from django.test import TestCase
from tests.factories.goal import GoalFactory

class GoalModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Goal = GoalFactory._meta.model
    def test_crud_goal(self):

        # CREATE (default)
        goal = GoalFactory()

        # READ
        self.assertEqual(goal.plat.name, 'This is a plat')
        self.assertEqual(goal.date, None)
        self.assertEqual(goal.count, 5)
        self.assertEqual(goal.pk, goal.id)

        # UPDATE
        goal.count = 10
        goal.plat.name = "Goal's plat"
        self.assertEqual(goal.count, 10)
        self.assertEqual(goal.plat.name, "Goal's plat") 
from django.test import TestCase
from tests.factories.owner import OwnerFactory

class OwnerModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Owner = OwnerFactory._meta.model
    def test_crud_owner(self):
        # CREATE
        owner = OwnerFactory()

        # READ (default)
        self.assertEqual(owner.name, 'X Owner')
        self.assertEqual(owner.pk, owner.id)
        
        # UPDATE
        owner.name = 'Y Owner'
        self.assertEqual(owner.name, 'Y Owner')
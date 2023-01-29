from django.test import TestCase
from tests.factories.partner import PartnerFactory

class PartnerModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Partner = PartnerFactory._meta.model
    def test_crud_partner(self):
        # CREATE without arguments
        partner = PartnerFactory()

        # READ default
        self.assertEqual(partner.name, 'X Partner')
        self.assertEqual(partner.pk, partner.id)
        
        # UPDATE
        partner.name = 'Y Partner'
        self.assertEqual(partner.name, 'Y Partner')
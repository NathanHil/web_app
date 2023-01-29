from django.test import TestCase
from tests.factories.community import CommunityFactory

class CommunityModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Community = CommunityFactory._meta.model
    def test_crud_community(self):
        # CREATE
        community = CommunityFactory(name='X Community')

        # READ
        self.assertEqual(community.name, 'X Community')
        self.assertEqual(community.abbreviation, 'XC')
        self.assertEqual(community.excise_tax_rate, 0.00)
        self.assertEqual(community.sales_tax_rate, 0.00)
        self.assertEqual(community.city, 'Bend')
        self.assertEqual(community.state, 'OR')
        self.assertEqual(community.zip_code, '97701')
        self.assertEqual(community.pk, community.id)
        
        # UPDATE
        community.name = 'Y Community'
        community.abbreviation = 'YC'
        self.assertEqual(community.name, 'Y Community')
        self.assertEqual(community.abbreviation, 'YC')

    # name = 'X Community'
    # city = 'Bend'
    # state = 'OR'
    # zip_code = 97701
from django.test import TestCase
from tests.factories.plat import PlatFactory

class PlatModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Plat = PlatFactory._meta.model
    def test_crud_plat(self):

        # CREATE (default)
        plat = PlatFactory()

        # READ
        self.assertEqual(plat.partner.name, 'X Partner')
        self.assertEqual(plat.name, 'This is a plat')
        self.assertEqual(plat.build_order, 0)
        self.assertEqual(plat.date_posted, None)
        self.assertEqual(plat.community.name, 'X Community')
        self.assertFalse(plat.schedule_found)
        self.assertEqual(plat.default_start_pace, 0)
        self.assertEqual(plat.est_vert_start_date, None)
        self.assertEqual(plat.planned_vert_start_date, None)
        self.assertEqual(plat.pk, plat.id)
        # Read class methods
        #no data to "Sum" in lot_count() method
        # self.assertEqual(plat.lot_count(), None) #Lot count no longer exists

        # UPDATE
        plat.name = 'This might also be a plat'
        plat.partner.name = "Plat's partner"
        plat.community.name = "Plat's community"
        self.assertEqual(plat.name, 'This might also be a plat')
        self.assertEqual(plat.partner.name, "Plat's partner")
        self.assertEqual(plat.community.name, "Plat's community")
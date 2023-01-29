from django.test import TestCase
from tests.factories.traffic import TrafficFactory

class TrafficModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Traffic = TrafficFactory._meta.model
    def test_crud_traffic(self):
        # CREATE
        traffic = TrafficFactory()

        # READ
        self.assertEqual(traffic.plat.name, 'This is a plat')
        self.assertEqual(traffic.count, 123)
        self.assertEqual(traffic.be_back_count, 0)
        self.assertEqual(traffic.date, None)
        self.assertEqual(traffic.pk, traffic.id)

        # UPDATE
        traffic.count = 321
        traffic.plat.name = "Lender's plat"
        self.assertEqual(traffic.count, 321)
        self.assertEqual(traffic.plat.name, "Lender's plat")
from django.test import TestCase
from tests.factories.job import JobFactory
from tests.factories.phase import PhaseFactory
from tests.factories.building_permit import BuildingPermitFactory


class BuildingPermitModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.BuildingPermit = BuildingPermitFactory._meta.model
        cls.Job = JobFactory._meta.model

    def test_crud_building_permit(self):
        # CREATE (default)
        building_permit = BuildingPermitFactory()
        building_permit.job = JobFactory(number="123-45-678")
        building_permit.job.phase = PhaseFactory(number=5, name='job phase')

        # READ
        self.assertEqual(building_permit.job.number, "123-45-678")
        self.assertEqual(building_permit.job.phase.name, 'job phase')
        self.assertEqual(building_permit.job.lot_number, 420)
        self.assertEqual(building_permit.submission_date, "")
        self.assertEqual(building_permit.status, None)
        self.assertEqual(building_permit.number, 321)
        self.assertEqual(building_permit.note, "Hello World")

        # UPDATE
        building_permit.job.lot_number = 111
        building_permit.job.phase.name = "Building permit's Job's phase"
        building_permit.status = "Complete"
        self.assertEqual(building_permit.job.lot_number, 111)
        self.assertEqual(building_permit.job.phase.name, "Building permit's Job's phase")
        self.assertEqual(building_permit.status, "Complete")
        self.assertIsNot(building_permit.note, "Changed note!!")

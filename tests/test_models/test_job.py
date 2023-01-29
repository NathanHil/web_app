from django.test import TestCase
from tests.factories.job import JobFactory
from tests.factories.phase import PhaseFactory
from tests.factories.plan import PlanFactory

class JobModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Job = JobFactory._meta.model
        cls.Phase = PhaseFactory._meta.model
        cls.Plan = PlanFactory._meta.model
    def test_crud_job(self):
        # CREATE (default)
        job = JobFactory()
        job.phase = PhaseFactory(number=20, name='job phase')
        job.plan = PlanFactory()
        
        # READ
        self.assertEqual(job.phase.name, 'job phase')
        self.assertEqual(job.lot_number, 420)
        self.assertEqual(job.number, '000-00-000')
        self.assertEqual(job.sales_status, '')
        self.assertEqual(job.construction_status, None)
        self.assertEqual(job.category, None)
        self.assertEqual(job.plan.name, 'X Plan')
        self.assertEqual(job.actual_sale_date, None)
        self.assertEqual(job.actual_start_date, None)
        self.assertEqual(job.actual_closing_date, None)
        self.assertEqual(job.actual_completion_date, None)
        self.assertEqual(job.projected_sale_date, None)
        self.assertEqual(job.projected_start_date, None)
        self.assertEqual(job.projected_closing_date, None)
        self.assertEqual(job.projected_completion_date, None)
        self.assertEqual(job.elevation, None)
        self.assertEqual(job.garage_orientation, None)
        self.assertEqual(job.attached_count, 0)
        self.assertEqual(job.garage_add, None)
        self.assertEqual(job.sales_price, 100000.00)
        self.assertEqual(job.lot_premium, 0)
        self.assertEqual(job.pk, job.id)

        # UPDATE
        job.lot_number = 420
        job.phase.name = "Job's phase"
        job.plan.name = 'Y Plan'
        self.assertEqual(job.lot_number, 420)
        self.assertEqual(job.phase.name, "Job's phase")
        self.assertEqual(job.plan.name, 'Y Plan')
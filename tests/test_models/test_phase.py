from django.test import TestCase
from tests.factories.phase import PhaseFactory
from tests.factories.plat import PlatFactory


class PhaseModelsTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.Phase = PhaseFactory._meta.model

	def test_crud_phase(self):
		# CREATE
		phase = PhaseFactory(name='new phase')
		phase.plat = PlatFactory()

		# READ
		self.assertEqual(phase.number, 10)
		self.assertEqual(phase.name, 'new phase')
		self.assertEqual(phase.lot_count, 0)
		self.assertEqual(phase.plat.name, "This is a plat")
		self.assertEqual(phase.owner.name, "X Owner")
		self.assertEqual(phase.pk, phase.id)

		# UPDATE
		phase.name = "This is a new phase"
		phase.plat.name = "This is a new plat"
		phase.owner.name = "Y Owner"
		self.assertEqual(phase.name, "This is a new phase")
		self.assertEqual(phase.plat.name, "This is a new plat")
		self.assertEqual(phase.owner.name, "Y Owner")

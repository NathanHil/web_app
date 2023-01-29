from django.test import TestCase
from tests.factories.projectedstart import ProjectedStartFactory
from tests.factories.plat import PlatFactory
from tests.factories.community import CommunityFactory

class ProjectedStartModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ProjectedStart = ProjectedStartFactory._meta.model
        cls.Plat = PlatFactory._meta.model
    def test_crud_projected_start(self):
        # CREATE (default)
        PS = ProjectedStartFactory(
            plat=PlatFactory(
                community=CommunityFactory()
                )
            )
        
        # READ
        self.assertEqual(PS.plat.name, 'This is a plat')
        self.assertEqual(PS.month, None)
        self.assertEqual(PS.count, 5)
        self.assertEqual(PS.source, "naturally")
        self.assertEqual(PS.pk, PS.id)

        # UPDATE
        PS.count = 2
        PS.plat.name = "ProjectedStart's plat"
        self.assertEqual(PS.count, 2)
        self.assertEqual(PS.plat.community.name, 'X Community')
        self.assertEqual(PS.plat.name, "ProjectedStart's plat")
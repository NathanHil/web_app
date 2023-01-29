import factory
import django
from blog.models import BuildingPermit 
from tests.factories.job import JobFactory

class BuildingPermitFactory(factory.Factory):
	class Meta:
		model = BuildingPermit

	job = JobFactory(number='123-45-678')
	submission_date = ''
	status = None
	number = 321
	note = 'Hello World'
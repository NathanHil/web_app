import factory
import django
from blog.models import Owner

class OwnerFactory(factory.Factory):
	class Meta:
		model = Owner

	name = 'X Owner'
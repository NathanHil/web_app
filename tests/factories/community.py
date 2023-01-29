import factory
import django
from blog.models import Community

class CommunityFactory(factory.Factory):
    class Meta:
        model = Community

    name = 'X Community'
    abbreviation = 'XC'
    city = 'Bend'
    state = 'OR'
    zip_code = '97701'

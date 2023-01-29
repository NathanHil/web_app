import factory
import django
from blog.models import Plan

class PlanFactory(factory.Factory):
    class Meta:
        model = Plan

    name = 'X Plan'
    size = 100
    is_active = False
    stories = 2
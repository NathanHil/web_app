import factory
from django.contrib.auth import get_user_model
from faker import Factory
from blog.models import Plat
from django.contrib.auth.models import User

User = get_user_model()

faker = Factory.create()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = faker.name()
    email = faker.email()

class PlatFactory(factory.Factory):
    class Meta:
        model = Plat
    name = faker.text()
    author = factory.SubFactory(UserFactory)
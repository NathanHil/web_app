from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Factory

from blog.models import Plat
from tests.factories.view import PlatFactory, UserFactory
from blog.models import Plat

User = get_user_model()

class PlatListViewTests(TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.plat = PlatFactory(author=self.author)
        self.url = reverse(
            'plat:plat-home', 
             args=(self.author.id,)
        )
    def test_with_several_plat_by_one_user(self):
        plat1 = PlatFactory(author=self.author)
        plat2 = PlatFactory(author=self.author)
        plat3 = PlatFactory(author=self.author)
        plat4 = PlatFactory(author=self.author)
        plat5 = PlatFactory(author=self.author)
        
        #response = self.plat.get_absolute_url(self)
        response = self.plat.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, plat1.name)
        self.assertContains(response, plat2.name)
        self.assertContains(response, plat3.name)
        self.assertContains(response, plat4.name)
        self.assertContains(response, plat5.name)
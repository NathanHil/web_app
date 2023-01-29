from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from blog.views import TieOutProgressView, TieoutView

class TieoutProgressTest(TestCase):
	def setUp(self):
		# Every test needs access to the request factory
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='nathan', email='nathan@...', password='top_secret')

	def test_tieout(self):
		# Create an instance of a GET request using RequestFactory()
		request = self.factory.get('/tieout/')
		view = TieOutProgressView()
		view.setup(request)

		# middleware are not supported. You can simulate a logged-in user by setting request.user manually
		request.user = self.user

		# Test TieoutView() as if it were deployed at /tieout
		# Use this syntax for class-based views
		response = TieOutProgressView.as_view()(request)
		self.assertEqual(response.status_code, 200)

	def test_tieout_view(self):
		request = self.factory.get('/tieout/2992')
		view = TieoutView()
		view.setup(request=request, pk=2992)

		request.user = self.user

		response = TieoutView.as_view()(request=request, pk=2992)
		self.assertEqual(response.status_code, 200)
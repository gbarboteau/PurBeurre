from django.test import TestCase
from django.urls import reverse
from .models import Category, Aliment, Substitute
from django.contrib.auth.models import User


# Create your tests here.
class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ModelsTestCase(TestCase):

	def test_aliment_object(self):
		aliment = Aliment.objects.create(name="Chou Rouge")
		self.assertIs(aliment.name, "Chou Rouge")

	def test_substitute_object(self):
		test_user = User.objects.create(username='Testuser')
		test_aliment = Aliment.objects.create(name="Chou Rouge")
		test_substitute = Substitute.objects.create(user_id=test_user, aliment_id=test_aliment)
		self.assertSequenceEqual([test_user.id, test_aliment.id], [test_substitute.user_id_id, test_substitute.aliment_id_id])

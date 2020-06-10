from django.test import TestCase
from django.urls import reverse
from .models import Category, Aliment, Substitute

# Create your tests here.
class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class AlimentPageTestCase(TestCase):

    # ran before each test.
    def setUp(self):
        impossible = Aliment.objects.create(name="Chou Rouge", picture="", category="")
        self.aliment = Aliment.objects.get(name="Chou Rouge")
        print("c'est gagné")

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        aliment_id = self.aliment.id
        response = self.client.get(reverse('aliment', args=(aliment_id,)))
        print(response['location'])
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the items does not exist
    def test_detail_page_returns_404(self):
        aliment_id = self.aliment.id + 1
        response = self.client.get(reverse('aliment', args=(aliment_id,)))
        self.assertEqual(response.status_code, 404)

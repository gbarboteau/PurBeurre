from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Category, Aliment, Substitute
from django.contrib.auth.models import User


# Create your tests here.
class IndexPageTestCase(TestCase):

    def test_index_page(self):
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


class UserCreationTestCase(TestCase):

    def test_create_account_page(self):
        response = self.client.get(reverse('create-account'))
        self.assertEqual(response.status_code, 200)

    def test_account_creation(self):
        response = self.client.post(reverse('create-account'), {'username':"Yoshi54", 'email':"yoshi54@caramail.com", 'password1':"FANDECYRILHANOUNA", 'password2':"FANDECYRILHANOUNA"})
        self.assertEqual(response.status_code, 200)


class UserLoginTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()

    def test_sign_in_page(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_signing_in(self):
        response = self.client.post(reverse('account'), {'username':"Yoshi54", 'password':"FANDECYRILHANOUNA"})
        self.assertEqual(response.status_code, 200)


class LogoutTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")

    def test_logout_page(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class SearchTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()

    def test_search_page_not_logged_in(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 302)

    def test_search_page_logged_in(self):
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)


class AlimentTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()
        aliment = Aliment.objects.create(name="Chou Rouge")
        aliment.save()

    def test_aliment_wrong_page(self):
        aliment = Aliment.objects.get(name="Chou Rouge")
        aliment_id = aliment.id + 1
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get('/aliment/' + str(aliment_id) + '/')
        self.assertEqual(response.status_code, 404)

    def test_aliment_page_not_logged_in(self):
        aliment = Aliment.objects.get(name="Chou Rouge")
        aliment_id = aliment.id
        response = self.client.get('/aliment/' + str(aliment_id) + '/')
        self.assertEqual(response.status_code, 302)

    def test_aliment_page_logged_in(self):
        aliment = Aliment.objects.get(name="Chou Rouge")
        aliment_id = aliment.id
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get('/aliment/' + str(aliment_id) + '/')
        self.assertEqual(response.status_code, 200)


class MesProduitsTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()

    def test_mesproduits_page_not_logged_in(self):
        response = self.client.get(reverse('mesproduits'))
        self.assertEqual(response.status_code, 302)

    def test_mesproduits_page_logged_in(self):
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('mesproduits'))
        self.assertEqual(response.status_code, 200)


class MentionsLegalesTestCase(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('mentionslegales'))
        self.assertEqual(response.status_code, 200)

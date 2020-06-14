from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Category, Aliment, Substitute
from django.contrib.auth.models import User


class IndexPageTestCase(TestCase):
    """Tests of the index view"""
    def test_index_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ModelsTestCase(TestCase):
    """Tests of the models"""
    def test_aliment_object(self):
        """Test of the aliment model"""
        aliment = Aliment.objects.create(name="Chou Rouge")
        self.assertIs(aliment.name, "Chou Rouge")

    def test_substitute_object(self):
        """Test of the substitute model"""
        test_user = User.objects.create(username='Testuser')
        test_aliment = Aliment.objects.create(name="Chou Rouge")
        test_substitute = Substitute.objects.create(user_id=test_user, aliment_id=test_aliment)
        self.assertSequenceEqual([test_user.id, test_aliment.id], [test_substitute.user_id_id, test_substitute.aliment_id_id])


class UserCreationTestCase(TestCase):
    """Tests of the create-account view"""
    def test_create_account_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('create-account'))
        self.assertEqual(response.status_code, 200)

    def test_account_creation(self):
        """Checks if users can create an account"""
        response = self.client.post(reverse('create-account'), {'username':"Yoshi54", 'email':"yoshi54@caramail.com", 'password1':"FANDECYRILHANOUNA", 'password2':"FANDECYRILHANOUNA"})
        self.assertEqual(response.status_code, 200)


class UserLoginTestCase(TestCase):
    """Tests of the account view"""
    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()

    def test_sign_in_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_signing_in(self):
        """Checks if users can log in"""
        response = self.client.post(reverse('account'), {'username':"Yoshi54", 'password':"FANDECYRILHANOUNA"})
        self.assertEqual(response.status_code, 200)


class LogoutTestCase(TestCase):
    """Tests of the logout view"""
    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")

    def test_logout_page(self):
        """Checks if users can log out"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class SearchTestCase(TestCase):
    """Tests of the index view"""
    def setUp(self):
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()

    def test_search_page_not_logged_in(self):
        """Checks if the page is not accessible when
        users aren't logged in
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 302)

    def test_search_page_logged_in(self):
        """Checks if the page is accessible when
        users are logged in
        """
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)


class AlimentTestCase(TestCase):

    def setUp(self):
        """Setting up the tests"""
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()
        aliment = Aliment.objects.create(name="Chou Rouge")
        aliment.save()

    def test_aliment_wrong_page(self):
        """Checks if the page is not accessible when
        you try to access a non-existing aliment
        """
        aliment = Aliment.objects.get(name="Chou Rouge")
        aliment_id = aliment.id + 1
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get('/aliment/' + str(aliment_id) + '/')
        self.assertEqual(response.status_code, 404)

    def test_aliment_page_not_logged_in(self):
        """Checks if the page is not accessible when
        users aren't logged in
        """
        aliment = Aliment.objects.get(name="Chou Rouge")
        aliment_id = aliment.id
        response = self.client.get('/aliment/' + str(aliment_id) + '/')
        self.assertEqual(response.status_code, 302)

    def test_aliment_page_logged_in(self):
        """Checks if the page is accessible when
        users are logged in
        """
        aliment = Aliment.objects.get(name="Chou Rouge")
        aliment_id = aliment.id
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get('/aliment/' + str(aliment_id) + '/')
        self.assertEqual(response.status_code, 200)


# class AddSubstituteTestCase(TestCase):

    

    # def setUp(self):
        # self.factory = RequestFactory()
        # user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        # user.save()
        # aliment1 = Aliment.objects.create(name="Coca-Cola", category="Soda", nutriscore="e")
        # aliment1.save()
        # aliment2 = Aliment.objects.create(name="Coca Light", category="Soda", nutriscore="d")
        # aliment2.save()

    # def test_add_substitute_not_logged_in(self):
    #     pass

    # def test_add_substitute_logged_in(self):
    #     user = User.objects.create_user('Yoshi54', 'yoshi54@caramail.com', 'FANDECYRILHANOUNA')
    #     self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
    #     # request = self.factory.get('/')        # or any other methods
    #     # request.user = User.objects.get(username="Yoshi54")
    #     print(str(user.id) + " est connecté")
    #     aliment = Aliment.objects.get_or_create(name="Coca Light")[0]
    #     aliment.save()
    #     substitute = Substitute(user_id=user, aliment_id=aliment)
    #     substitute.save()
    #     print(str(user.id) + " est connecté")
    #     # query = request.POST.get(substitute, False)
    #     # my_substitute = Substitute.objects.get(aliment_id=aliment)
    #     response = self.client.post(reverse('add_product'), {'query': aliment})
    #     self.assertEqual(response.status_code, 200)


class MesProduitsTestCase(TestCase):
    """Tests of the mesproduits view"""
    def setUp(self):
        """Setting up the tests"""
        user = User.objects.create_user(username="Yoshi54", email="yoshi54@caramail.com", password="FANDECYRILHANOUNA")
        user.save()

    def test_mesproduits_page_not_logged_in(self):
        """Checks if the page is not accessible when
        users aren't logged in
        """
        response = self.client.get(reverse('mesproduits'))
        self.assertEqual(response.status_code, 302)

    def test_mesproduits_page_logged_in(self):
        """Checks if the page is accessible when
        users are logged in
        """
        self.client.login(username="Yoshi54", password="FANDECYRILHANOUNA")
        response = self.client.get(reverse('mesproduits'))
        self.assertEqual(response.status_code, 200)


class MentionsLegalesTestCase(TestCase):
    """Tests of the mentionslegales view"""
    def test_index_page(self):
        """Checks if the page is accessible"""
        response = self.client.get(reverse('mentionslegales'))
        self.assertEqual(response.status_code, 200)

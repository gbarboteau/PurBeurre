from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from application.models import Category, Aliment, Substitute
import requests
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.collect_data()

    def collect_data(self):
        all_categories = Category.objects.all()
        self.category_data = []
        for category in all_categories:
            print(category.category_name)
            self.category_data.append(self.category_scrapper(category.category_name))
            self.data = self.category_data
            for i in self.data:
                for j in i:
                    if j is not None:
                        if 'product_description' in j and 'barcode' in j and 'product_name' in j and 'nutriscore' in j and 'stores' in j and 'product_category' in j and 'picture' in j:
                            self.put_it_in_tables(i[0])


    def category_scrapper(self, category):
        fullRequest = requests.get('https://fr.openfoodfacts.org/categorie/' + str(category) + '.json')
        readableRequest = json.loads(fullRequest.text)
        cleanedData = self.clean_data(readableRequest, category)
        return cleanedData

    def clean_data(self, data, category):
        my_ids = []
        all_ids = len(data['products'])
        for i in range(all_ids):
            my_ids.append(data['products'][i]['_id'])
        my_products = []
        for i in my_ids:
            my_products.append(self.aliment_scrapper(i, category))
        return my_products

    def aliment_scrapper(self, barcode, category):
        aliment_fullRequest = requests.get("https://fr.openfoodfacts.org/api/v0/product/" + barcode + ".json")
        aliment_readableRequest = json.loads(aliment_fullRequest.text)
        aliment_cleanedData = self.clean_data_aliment(aliment_readableRequest, category)
        return aliment_cleanedData

    def clean_data_aliment(self, my_dict, category):
        """Create a list of readable data
        for a given product.
        """
        my_data = {}
        all_the_data = my_dict['product']
        my_data['product_name'] = self.does_exist_in_dict('product_name_fr', all_the_data)
        my_data['product_description'] = self.does_exist_in_dict('ingredients_text', all_the_data)
        my_data['barcode'] = self.does_exist_in_dict('id', all_the_data)
        my_data['nutriscore'] = self.does_exist_in_dict('nutrition_grade_fr', all_the_data)
        my_data['stores'] = self.does_exist_in_dict('stores', all_the_data)
        my_data['product_category'] = category
        my_data['picture'] = self.does_exist_in_dict('image_front_url', all_the_data)
        if my_data['product_description'] == "":
            my_data['product_description'] = "Pas de description disponible"
        if my_data['stores'] == "":
            my_data['stores'] = "Pas de magasins disponibles"
        # print(my_data)
        if "NONE" in my_data.values() or "" in my_data.values():
            return None
        else:
            return my_data

    def put_it_in_tables(self, new_data):
        my_data = new_data
        if my_data is None:
            pass
        else:
            if my_data['product_description'] is None:
                my_data['product_description'] = "Pas de description disponible"
            elif my_data['product_description'] == "":
                my_data['product_description'] = "Pas de description disponible"
            if my_data['stores'] is None:
                my_data['stores'] = "Pas de magasins disponibles"
            elif my_data['stores'] == "":
                my_data['stores'] = "Pas de magasins disponibles"
            # print(my_data)
            if "NONE" in my_data.values() or "" in my_data.values():
                pass
            else:
                try:
                    new_aliment = Aliment.objects.get_or_create(name=my_data['product_name'], category=my_data['product_category'], picture=my_data['picture'], nutriscore=my_data['nutriscore'], description=my_data['product_description'], barcode=my_data['barcode'], stores=my_data['stores'])
                except IntegrityError as error:
                    pass

    def does_exist_in_dict(self, my_key, my_dict):
        """Check if a key exists in a given dict."""
        if my_key in my_dict:
            return my_dict[my_key]
        else:
            return "NONE"
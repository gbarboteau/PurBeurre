"""Collects the data from the OpenFoodFacts API.
"""
import requests
import json
import psycopg2

import util


class DataCollecter:
    """Creates instances of CategoryScrapper to 
    collect datas from food categories.
    """
    def __init__(self, my_auth):
        """Creates an instance of DataCollecter, 
        which then creates instances of 
        CategoryScrapper, and put returned
        informations in a list.
        """
        self.user = my_auth.user
        self.password = my_auth.password
        my_connection = psycopg2.connect(user=my_auth.user, password=my_auth.password, host = "127.0.0.1", port = "5432", database='purbeurre')
        cursor = my_connection.cursor()
        self.categories = []
        query = ('SELECT category_name FROM application_category ')
        cursor.execute(query)
        for category_name in cursor:
            self.categories.append(category_name[0])
        cursor.close()
        my_connection.close()
        self.category_scrapper = []
        for i in self.categories:
            self.category_scrapper.append(CategoryScrapper(i))
        self.data = self.category_scrapper
        self.my_data = []
        for i in self.data:
            for j in i.cleanedData:
                if j.cleanedData:
                    self.my_data.append(j.cleanedData)


class CategoryScrapper:
    """Create instances of ProductScrapper which
    collects informations of every product in
    the category.
    """
    def __init__(self, my_category):
        """Create an instance of CategoryScrapper"""
        self.fullRequest = requests.get('https://fr.openfoodfacts.org/categorie/' + my_category + '.json')
        self.readableRequest = json.loads(self.fullRequest.text)
        self.cleanedData = self.clean_data(self.readableRequest, my_category)

    def clean_data(self, my_dict, my_category):
        """Create a list of readable data
        by creating a ProductScrapper instance
        for every product in the category.
        """
        my_ids = []
        all_ids = len(my_dict['products'])
        for i in range(all_ids):
            my_ids.append(my_dict['products'][i]['_id'])
        my_products = []
        for i in my_ids:
            my_products.append(ProductScrapper(i, my_category))
        return my_products


class ProductScrapper:
    """Collect informations about a given
    product.
    """
    def __init__(self, barcode, my_category):
        """Create an instance of ProductScrapper"""
        self.fullRequest = requests.get("https://world.openfoodfacts.org/api/v0/product/" + barcode + ".json")
        self.readableRequest = json.loads(self.fullRequest.text)
        self.cleanedData = self.clean_data(self.readableRequest, my_category)

    def clean_data(self, my_dict, my_category):
        """Create a list of readable data
        for a given product.
        """
        my_data = {}
        all_the_data = my_dict['product']
        my_data['product_name'] = util.does_exist_in_dict('product_name_fr', all_the_data)
        my_data['product_description'] = util.does_exist_in_dict('ingredients_text', all_the_data)
        my_data['barcode'] = util.does_exist_in_dict('id', all_the_data)
        my_data['nutritional_score'] = util.does_exist_in_dict('nutrition_grade_fr', all_the_data)
        my_data['stores'] = util.does_exist_in_dict('stores', all_the_data)
        my_data['product_category'] = my_category
        my_data['picture'] = util.does_exist_in_dict('image_front_url', all_the_data)
        if my_data['product_description'] == "":
            my_data['product_description'] = "Pas de description disponible"
        if my_data['stores'] == "":
            my_data['stores'] = "Pas de magasins disponibles"
        if "NONE" in my_data.values() or "" in my_data.values():
            return None
        else:
            return my_data

"""Fill the database with the data collected by
datacollecter.py
"""
import psycopg2


class Filler:
    """Adds a set of data in the openfoodfacts
    database. Needs to be authentificated.
    """
    def __init__(self, my_data, my_auth):
        """Create an instance of Filler"""
        self.user = my_auth.user
        self.password = my_auth.password
        self.my_data = my_data

    def put_it_in_tables(self):
        """Put all the data given at the instance creation
        into the database.
        """
        my_connection = psycopg2.connect(user=self.user, password=self.password, host = "127.0.0.1", port = "5432", database='purbeurre')
        cursor = my_connection.cursor()
        for i in self.my_data:
            prod_name = i['product_name']
            print(prod_name)
            try:
                add_aliment = ('INSERT INTO aliment '
                       '(product_name, product_description, barcode, nutritional_score, stores, product_category, picture) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s)')
                data_aliment = (i['product_name'].replace("'", "''"), i['product_description'].replace("'", "''"), i['barcode'].replace("'", "''"), i['nutritional_score'].replace("'", "''"), i['stores'].replace("'", "''"), i['product_category'].replace("'", "''"), i['picture'].replace("'", "''"))
                cursor.execute(add_aliment, data_aliment)
            except psycopg2.IntegrityError:
                print("erreur sur " + prod_name)
                my_connection.rollback()
        my_connection.commit()
        cursor.close()
        my_connection.close()
        print("ok c'est fait")

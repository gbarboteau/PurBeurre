"""The program filling the openfoodfacts database
with entries for its different categories.
"""
import argparse
import getpass
import psycopg2

import datacollecter
import filler
import auth


def main():
    """Checks for a matching username/password
    combination, then fill the openfoodfacts database.
    """
    parser = argparse.ArgumentParser()
    my_auth = auth.Auth()
    parser.add_argument("user", help="is the user for the database")
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    try:
        my_connection = psycopg2.connect(user=my_auth.user, password=my_auth.password, host = "127.0.0.1", port = "5432", database='purbeurre')
        print("1")
        my_connection.close()
        print("2")
        dt = datacollecter.DataCollecter(my_auth)
        print("3")
        my_data = dt.my_data
        print("4")
        fil = filler.Filler(my_data, my_auth)
        print("5")
        fil.put_it_in_tables()
        print("6")
    except Exception as error:
        print("Oops, something happened: ", error)

main();

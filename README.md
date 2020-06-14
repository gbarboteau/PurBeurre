### Setup

Please use the 3.8 version of Python.

Download the repo :
- `git clone https://github.com/gbarboteau/PurBeurre.git`

Use a virtual environment and install the requirement:
- `pip install -r requirements.txt`

### Add a food category

You can add a food category to search in the OpenFoodFacts database with this command:
- `python manage.py createcategory category-name category-url`

### Update the application database

You can update the database with this command:
- `python manage.py updatebdd`

### Launch the app (locally)

- `python manage.py runserver`

And go to the 127.0.0.1:8000 url.
"""Handles the user authentification
User's username and password need to match
a MySQL's already created profile
(see the README for more info)
"""
class Auth:
    """A token identifying the current user"""
    def __init__(self):
        """The user is identified with its username 
        and password (must match the database)
        """
        self.user = ""
        self.password = ""
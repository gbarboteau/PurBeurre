"""Some useful functions abstract enough
to be used into several scripts.
"""
def does_exist_in_dict(my_key, my_dict):
    """Check if a key exists in a given dict."""
    if my_key in my_dict:
        return my_dict[my_key]
    else:
        return "NONE"

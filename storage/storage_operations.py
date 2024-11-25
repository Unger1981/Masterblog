import os
import json

file_path = os.path.join("storage", "storage.json")

def load_json():
    """
    Loads blog posts from the JSON file.

    Attempts to open the JSON file and load the blog posts. 
    If an error occurs (e.g., JSON error or file not found), 
    an empty list is returned and an error message is printed.

    Returns:
        list: A list of blog posts (or an empty list in case of an error).
    """
    try:
        with open(file_path, "r") as file:
            blog_posts = json.load(file)
            return blog_posts
    except json.JSONDecodeError as e:
        print(f"Failed to load JSON. Error: {e}")
        blog_posts = []
        return blog_posts
    except FileNotFoundError as e:
        print(f"File not found. Error: {e}")
        blog_posts = []
        return blog_posts


def save_json(blog_posts):
    """
    Saves blog posts to the JSON file.

    Attempts to write the blog posts as JSON to the file. If an error occurs 
    (e.g., file not found or write error), an error message is printed.

    Args:
        blog_posts (list): A list of blog posts to be saved.

    Returns:
        None
    """
    try:
        with open(file_path, "w") as file:
            json.dump(blog_posts, file, indent=4)
    except FileNotFoundError as e:
        print(f"File not found. Error: {e}")
    except (OSError, IOError) as e:
        print(f"Failed to write to JSON file. Error: {e}")

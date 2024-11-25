from flask import Flask, render_template, redirect, url_for, request
from storage.storage_operations import load_json, save_json
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    """
    Handle the root route ('/'). 
    Loads blog posts from the JSON file and renders the index template 
    with the posts. If an error occurs, it returns an empty list.

    Returns:
        Rendered template with blog posts.
    """
    try:
        blog_posts = load_json()
    except json.JSONDecodeError as e:
        print(f"Failed to load JSON. Error: {e}")
        blog_posts= []
    except FileNotFoundError:
        print("The file 'storage.json' was not found.")  
        blog_posts= [] 
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the '/add' route for both GET and POST requests.
    - For POST: Adds a new post or updates an existing one.
    - For GET: Renders the form to add a new post.

    Returns:
        Redirect to the index page if successful, 
        otherwise renders the 'addPost.html' template.
    """
    if request.method == 'POST':
        title = request.form.get("title", "unknown")
        author = request.form.get("author", "unknown")
        content = request.form.get("content", "unknown")
        try:
            post_id = int(request.form.get("post_id", 0))
        except ValueError:
            post_id = 0    
        
        try:
            blog_posts = load_json()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading JSON: {e}")
            blog_posts = []
        if post_id == 0:
            post_id = len(blog_posts) + 1
            while True:
                for post in blog_posts:
                    if post["id"] == post_id:
                        post_id += 1
                else:
                    break

            new_post = {"id": post_id, "author": author, "title": title, "content": content}
            blog_posts.append(new_post)
        else:
            for post in blog_posts:
                if post_id == post["id"]:
                    post["title"] = title
                    post["author"] = author
                    post["content"] = content
        save_json(blog_posts)
        return redirect(url_for('index')) 
    elif request.method == 'GET' and not request.args:
        print("elif")
        return render_template('addPost.html')        
    else:
        title = request.args.get('title', 'unknown')
        author = request.args.get('author', 'unknown')
        content = request.args.get('content', 'unknown')
        try:
            blog_posts = load_json()
            post_id = len(blog_posts) + 1
            new_post = {"id": post_id, "author": author, "title": title, "content": content}
            blog_posts.append(new_post)
            save_json(blog_posts)
            return redirect(url_for('index'))
        except json.JSONDecodeError as e:
            print(f"Failed to load JSON. Error: {e}")
        except FileNotFoundError  as e:
            print(f"File not found. Error: {e}")  
    return render_template('addPost.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Handle the '/delete/<post_id>' route.
    Deletes a blog post by its ID from the JSON file.

    Args:
        post_id (int): The ID of the blog post to be deleted.

    Returns:
        Redirects to the index page after deleting the post.
    """
    try:
        blog_posts = load_json()
        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
                break 
        save_json(blog_posts)
        return redirect(url_for('index'))  
    except Exception as e:
        print(e)
    

@app.route('/update/<int:post_id>')
def update(post_id):
    """
    Handle the '/update/<post_id>' route.
    Retrieves a blog post by its ID and renders the update form.

    Args:
        post_id (int): The ID of the blog post to be updated.

    Returns:
        Rendered template for updating the blog post with its current details.
    """
    try:
        blog_posts = load_json()
        for post in blog_posts:
            if post['id'] == post_id:
                title = post.get("title", "Untitled")
                author = post.get("author", "Untitled")
                content = post.get("content", "Untitled")
                break 
    except Exception as e:
        print(e)    
    return render_template('update.html', title = title, author = author, content = content, post_id = post_id)

    
if __name__ == '__main__':
    """
    Run the Flask application.

    Starts the Flask development server on host '0.0.0.0' and port 5000 
    with debugging enabled.
    """
    app.run(host="0.0.0.0", port=5000, debug=True)

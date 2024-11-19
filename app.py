from flask import Flask, render_template, redirect, url_for, request
import os
import json

app = Flask(__name__)
file_path= os.path.join("storage", "storage.json")


@app.route('/')
def index():
  
    try:
        with open(file_path, "r") as file:
            blog_posts = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Failed to load JSON. Error: {e}")
        blog_posts= []
    except FileNotFoundError:
        print("The file 'storage.json' was not found.")  
        blog_posts= [] 
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get("title", "unknown")
        author = request.form.get("author", "unknown")
        content = request.form.get("content", "unknown")
        try:
            with open(file_path, "r") as file:
                blog_posts = json.load(file)
            post_id = len(blog_posts) + 1
            new_post = {"id": post_id, "author": author, "title": title, "content": content}
            blog_posts.append(new_post)
            with open(file_path, "w") as file:
                json.dump(blog_posts, file, indent=4)
            return redirect(url_for('index'))
        except json.JSONDecodeError as e:
            print(f"Failed to load JSON. Error: {e}")
        except FileNotFoundError  as e:
            print(f"File not found. Error: {e}")  
    elif request.method == 'GET' and not request.args:
        return render_template('addPost.html')        
    else:
        title = request.args.get('title', 'unknown')
        author = request.args.get('author', 'unknown')
        content = request.args.get('content', 'unknown')
        try:
            with open(file_path, "r") as file:
                blog_posts = json.load(file)
            post_id = len(blog_posts) + 1
            new_post = {"id": post_id, "author": author, "title": title, "content": content}
            blog_posts.append(new_post)
            with open(file_path, "w") as file:
                json.dump(blog_posts, file, indent=4)
            return redirect(url_for('index'))
        except json.JSONDecodeError as e:
            print(f"Failed to load JSON. Error: {e}")
        except FileNotFoundError  as e:
            print(f"File not found. Error: {e}")  
    return render_template('addPost.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    try:
        # Open and read the existing blog posts
        with open(file_path, "r") as file:
            blog_posts = json.load(file)
        
        # Find and remove the post with the matching ID
        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
                break  # Exit the loop once the post is deleted
        
        # Save the updated list back to the file
        with open(file_path, "w") as file:
            json.dump(blog_posts, file, indent=4)
        
        return redirect(url_for('index'))  # Redirect to the index page after deletion
    
    except json.JSONDecodeError as e:
        print(f"Failed to load JSON. Error: {e}")
        return "Error: Unable to process the data."
    except FileNotFoundError as e:
        print(f"File not found. Error: {e}")
        return "Error: The storage file does not exist."

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
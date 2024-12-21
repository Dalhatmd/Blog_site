#!/usr/bin/env python3
from models.storage.db import DB
from models.user import User
from models.blogs import Blog

# Initialize DB
db = DB()

# Add a user
new_user = User(email="bobs@email.com", name="John Doe")
saved_user = db.add('User', new_user)
if not saved_user:
    print("Failed to create user")
    exit(1)

# Get user by email
user = db.get_by_field('User', 'email', "bobs@email.com")
if not user:
    print("Failed to retrieve user")
    exit(1)

# Create a blog
new_blog = Blog(title="My Blog", content="Content", user_id=user.id)
saved_blog = db.add('Blog', new_blog)
if not saved_blog:
    print("Failed to create blog")
    exit(1)

# Get all blogs for a user
user_blogs = db.get_all_by_field('Blog', 'user_id', user.id)
if not user_blogs:
    print("No blogs found for user")
    exit(1)

for blog in user_blogs:
    print(blog.content)

blog_to_update = saved_blog.id
success = db.update('Blog', blog_to_update, title="New Title", content="New Content")
if not success:
    print("Failed to update blog")
    exit(1)

# Delete the blog
"""success = db.delete('Blog', blog_to_update)
if not success:
    print("Failed to delete blog")
    exit(1)"""
#!/usr/bin/python3
""" Test for blog functionality """
from models.storage.db import DB
from models.user import User
from models.blogs import Blog

# Initialize database
db = DB()

# Create a test user
new_user = User(
    email="test@example.com",
    first_name="Test",
    last_name="User"
)
new_user.password = "securepassword"

# Add user to database
if db.add_user(new_user):
    print("User added successfully")

    # Retrieve the user from the database to ensure it is attached to a session
    retrieved_user = db.get_user_by_email(new_user.email)
    if not retrieved_user:
        print("Failed to retrieve user from the database")
    else:
        # Create a blog post for the retrieved user
        blog = db.create_blog(
            user_id=retrieved_user.id,
            title="My First Blog Post",
            content="This is the content of my first blog post."
        )

        if blog:
            print(f"Blog created successfully: {blog.title}")

            # Get all blogs for the user
            user_blogs = db.get_user_blogs(retrieved_user.id)
            print(f"User has {len(user_blogs)} blog posts")

            # Update the blog
            if db.update_blog(blog.id, content="new freaking content"):
                print("Blog updated successfully")

            # Get the updated blog
            updated_blog = db.get_blog(blog.id)
            if updated_blog:
                print(f"Updated content: {updated_blog.content}")

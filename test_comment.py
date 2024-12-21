#!/usr/bin/env python3
from models.storage.db import DB
from models.user import User
from models.blogs import Blog
from models.comments import Comment

def main():
    # Initialize DB
    db = DB()

    # Create a test user
    test_user = User(email="test@example.com", name="Test User")
    saved_user = db.add('User', test_user)
    if not saved_user:
        print("Failed to create user")
        return

    # Create a test blog
    test_blog = Blog(
        title="Test Blog",
        content="This is a test blog post",
        user_id=saved_user.id
    )
    saved_blog = db.add('Blog', test_blog)
    if not saved_blog:
        print("Failed to create blog")
        return

    # Create some test comments
    comment1 = Comment(
        content="First comment!",
        user_id=saved_user.id,
        blog_id=saved_blog.id
    )
    comment2 = Comment(
        content="Second comment!",
        user_id=saved_user.id,
        blog_id=saved_blog.id
    )
    
    # Save comments
    db.add('Comment', comment1)
    db.add('Comment', comment2)

    # Test retrieving comments
    blog_comments = db.get_all_by_field('Comment', 'blog_id', saved_blog.id)
    print(f"\nComments for blog '{saved_blog.title}':")
    for comment in blog_comments:
        print(f"- {comment.content}")

    # Test updating a comment
    if blog_comments:
        first_comment = blog_comments[0]
        db.update('Comment', first_comment.id, content="Updated first comment!")
        
        # Verify update
        updated_comment = db.get_by_field('Comment', 'id', first_comment.id)
        print(f"\nUpdated comment content: {updated_comment.content}")

    # Test deleting a comment
    if len(blog_comments) > 1:
        second_comment = blog_comments[1]
        db.delete('Comment', second_comment.id)
        
        # Verify deletion
        remaining_comments = db.get_all_by_field('Comment', 'blog_id', saved_blog.id)
        print(f"\nRemaining comments count: {len(remaining_comments)}")

    print("\nTest completed!")

if __name__ == "__main__":
    main()
from flask import jsonify, request
from models.storage.db import DB
from models.blogs import Blog
from api.v1.views import app_views
from ..auth.auth import token_required
from models.comments import Comment
from sqlalchemy.orm import joinedload


db = DB()

@app_views.route('/blogs', methods=['GET'], strict_slashes=False)
def show_blogs():
    blogs = db.get_all('Blog')
    if blogs:
        return jsonify([blog.to_dict() for blog in blogs])
    return jsonify([])

@app_views.route('/blogs', methods=['POST'], strict_slashes=False)
@token_required
def create_blog():
    input_user_id = request.user_id
    data = request.get_json()
    if not all(field in data for field in ['title', 'content']):
        return jsonify({'message': 'Missing required fields'}), 400
    blog = Blog(
        title=data['title'],
        content=data['content'],
        user_id=input_user_id
    )
    saved_blog = db.add('Blog', blog)
    return jsonify(saved_blog.to_dict()), 201

@app_views.route('/blogs/<blog_id>', methods=['GET'], strict_slashes=False)
def show_blog(blog_id):
    blog = db.get_by_field('Blog', 'id', blog_id)
    if not blog:
        return jsonify({'message': 'Blog not found'}), 404
    return jsonify(blog.to_dict())

@app_views.route('/blogs/<blog_id>', methods=['PUT'], strict_slashes=False)
@token_required
def update_blog(blog_id):
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'data not provided'}), 400
    db.update('Blog', blog_id, **data)
    return jsonify({'Message': 'Blog updated successfully'}), 200

@app_views.route('/blogs/<blog_id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_blog(blog_id):
    blog = db.get_by_field('Blog', 'id', blog_id)
    if not blog:
        return jsonify({'message': 'Blog not found'}), 404
    db.delete('Blog', blog_id)
    return jsonify({}), 200

@app_views.route('/blogs/<blog_id>/comments', methods=['GET'], strict_slashes=False)
def show_comments(blog_id):
    # get the session to avoid detachment
    session = db.get_session()
    blog = db.get_by_field('Blog', 'id', blog_id)
    if not blog:
        return jsonify({'message': 'Blog Not Found'})
    comments = session.query(Comment).filter(Comment.blog_id == blog_id).all()
    if not comments:
        return jsonify({})
    return jsonify([comment.to_dict() for comment in comments])

@app_views.route('/blogs/<blog_id>/comments', methods=['POST'], strict_slashes=False)
@token_required
def create_comment(blog_id):
    blog = db.get_by_field('Blog', 'id', blog_id)
    if not blog:
        return jsonify({'message': 'Blog not found'}), 404
    data = request.get_json()
    user_id=request.user_id
    if not all(field in data for field in ['content']):
        return jsonify({'message': 'Missing required fields'}), 400
    try:
        comment = Comment(
            content=data['content'],
            blog_id=blog_id,
            user_id=user_id
        )
        saved_comment = db.add('Comment', comment)
        if not saved_comment:
            return jsonify({'message': 'Failed to add comment'})
    except Exception as e:
        print('Exception occured: ', e)
        return jsonify({'message': 'An error occured'})
    return jsonify(saved_comment.to_dict())


@app_views.route('/blogs/<blog_id>/comments/<comment_id>', methods=['GET'], strict_slashes=False)
def show_comment(blog_id, comment_id):
    comment = db.get_by_field('Comment', 'id', comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404
    return jsonify(comment.to_dict())


@app_views.route('/blogs/<blog_id>/comments/<comment_id>', methods=['PUT'], strict_slashes=False)
@token_required
def update_comment(blog_id, comment_id):
    comment = db.get_by_field('Comment', 'id', comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404
    data = request.get_json()
    db.update('Comment', comment_id, **data)
    return jsonify({'message': 'Updated successfully'})


@app_views.route('/blogs/<blog_id>/comments/<comment_id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_comment(blog_id, comment_id):
    comment = db.get_by_field('Comment', 'id', comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404
    db.delete('Comment', comment_id)
    return jsonify({}), 200

from flask import (Flask,jsonify,
                   request, render_template,
                   url_for, redirect)
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv
from models.storage.db import DB
import requests

db = DB()

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
api_url = 'http://127.0.0.1:5000/api/v1'

@app.errorhandler(404)
def page_not_found(e):
    """ 404 error handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    """ 400 error handler
    """
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(e):
    """ 500 error handler
    """
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    """ 405 error handler
    """
    return jsonify({"error": "Method not allowed"}), 405

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    response = requests.get(f'{api_url}/blogs')
    if response.status_code == 200:
        blogs=response.json()
        for blog in blogs:
            user = db.get_by_field('User', 'id', blog['user_id'])
            blog['username'] = user.username
        return render_template('blogs.html', blogs=blogs)
    elif response.status_code == 404:
        return render_template('404.html')

@app.route('/blogs/<blog_id>')
def get_blog(blog_id):
    response  = requests.get(f'{api_url}/blogs/{blog_id}')
    if response.status_code == 404:
        return render_template('404.html'), 404
    if response.status_code != 200:
        return render_template('error.html'), response.status_code

    comments_response = requests.get(f'{api_url}/blogs/{blog_id}/comments')
    if comments_response.status_code != 200:
        comments = []
    else:
        comments = comments_response.json()

    blog = response.json()
    user = db.get_by_field('User', 'id', blog['user_id'])
    blog['username'] = user.username
    print(blog['username'])
    if not blog['username']:
        blog['username'] = user.email
        print(blog['username'])
    return render_template('blog_detail.html', blog=blog, comments=comments)
    
@app.route('/blogs/new', methods=['GET'])
def post_blog():
    return render_template('blog_form.html')

@app.route('/login', methods=['GET'])
def login():
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET'])
def get_profile():
    return render_template('profile_page.html')

@app.route('/user/blogs', methods=['GET'])
def user_blogs():
    return render_template('user_blogs.html')

@app.route('/blogs/<blog_id>/edit', methods=['GET'])
def edit_blog(blog_id):
    return render_template('edit_blog.html', blog_id=blog_id)

if __name__ == "__main__":
    host = getenv('BLOG_HOST', '0.0.0.0')
    port = getenv('BLOG_PORT', '5000')
    app.run(host=host, port=port, debug=True)

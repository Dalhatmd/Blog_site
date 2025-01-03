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
    """token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'message': 'Token required'}), 401
    
    token = token.split(' ')[1]
    title = request.json.get('title')
    content = request.json.get('content')

    if not title or not content:
        return jsonify({'message': 'Title and content of blog required'}), 400
    
    blog_data = {
        'title': title,
        'content': content
    }

    response = requests.post(
        f"{api_url}/blogs",
        headers={'Authorization': f'Bearer {token}'},
        json=blog_data
    )
    if response.status_code == 201:
        return redirect(url_for('home'))
    """"""return jsonify({'message': 'failed to create Blog'}), response.status_code"""
    

if __name__ == "__main__":
    host = getenv('BLOG_HOST', '0.0.0.0')
    port = getenv('BLOG_PORT', '5000')
    app.run(host=host, port=port, debug=True)

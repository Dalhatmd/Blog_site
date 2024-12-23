from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

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

if __name__ == "__main__":
    host = getenv('BLOG_HOST', '0.0.0.0')
    port = getenv('BLOG_PORT', '5000')
    app.run(host=host, port=port, debug=True)

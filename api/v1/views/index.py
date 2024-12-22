from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ Return status
    """
    return jsonify({"status": "OK"}), 200

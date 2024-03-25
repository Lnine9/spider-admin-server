from flask import request, make_response
from flask_cors import CORS
from router import register_blueprint
from utils.flask_ext.flask_app import FlaskApp

app = FlaskApp(__name__)
CORS(app)

register_blueprint(app)


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        return make_response()


if __name__ == '__main__':
    app.run(port=2024, debug=True)

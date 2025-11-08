from flask import Flask, jsonify,abort, render_template, request
from controlador_juego import init_routes
from models import db
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration



app = Flask(__name__)

sentry_sdk.init(
    dsn="https://a6bcdc545a463912f84e28d816232174@o4510321751556096.ingest.us.sentry.io/4510321757585408",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2004@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ inicializa la conexión con la app
db.init_app(app)

init_routes(app)


@app.errorhandler(BadRequest)
def error_400(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(MethodNotAllowed)
def handle_405(e):
    return render_template('405.html'), 405

@app.errorhandler(HTTPException)
def handle_api_error(e):
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify(code=e.code, name=e.name, description=e.description).data
        response.content_type = "application/json"
        return response
    return e

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Error interno del servidor: {e}")
    return render_template("500.html"), 500



@app.route("/error")
def error():
    1/0  #
    return "<p>error!</p>"



@app.route('/api/test400')
def test_400():
    abort(400, description="Solicitud incorrecta en el endpoint de prueba")

@app.route('/solo_get', methods=['GET'])
def solo_get():
    return "Solo puedes usar GET aquí"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=False)

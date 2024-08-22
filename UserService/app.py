from flask import Flask

from .aop.error_handler import initialize_error_handlers
from .routes.user_bp import user_blueprint
from models.database import initialize_db


app = Flask(__name__)
app.register_blueprint(user_blueprint)

initialize_error_handlers(app)
initialize_db()


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from .session import Session, engine
from .models.model import Base
from .blueprints.users import users_blueprint
from .errors.errors import ApiError

app = Flask(__name__)
app.register_blueprint(users_blueprint)

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
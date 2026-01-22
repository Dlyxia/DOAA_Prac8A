from flask import Flask
from flask_cors import CORS

#create the Flask app
app = Flask(__name__)
CORS(app)

# # load configuration from config.cfg
# app.config.from_pyfile('config.cfg')

from application import routes

if routes.model_server_base_url == "https://<your render url>.onrender.com":
    raise ValueError("ERROR: Please change the 'model_server_base_url' to your actual model server URL in application/routes.py!")

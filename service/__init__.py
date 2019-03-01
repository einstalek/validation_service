from cryptography.fernet import Fernet
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '58d737a3bfc1db9359c5a00bec2b15920d3eae7692a4cbba482de34a16e6ed24'
app.config['TOKEN_SECRET_KEY'] = Fernet.generate_key()
encoder = Fernet(app.config['TOKEN_SECRET_KEY'])

allowed_ips = ["127.0.0.1", "localhost", "192.168.0.101", "192.168.0.105", "192.168.0.100"]

from service import routes


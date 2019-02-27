from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '58d737a3bfc1db9359c5a00bec2b15920d3eae7692a4cbba482de34a16e6ed24'
app.config['TOKEN_SECRET_KEY'] = Fernet.generate_key()
encoder = Fernet(app.config['TOKEN_SECRET_KEY'])
allowed_ips = ["127.0.0.1", "localhost"]


def check_request_ip_addr(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        if request.remote_addr not in allowed_ips:
            return jsonify({})
        else:
            return func(*args, **kargs)
    return wrapper


@app.route("/", methods=["POST", "GET"])
@check_request_ip_addr
def encrypt():
    form = request.form.to_dict()
    username, token = form.get('username'), form.get('token')
    if username and not token:
        token = encoder.encrypt(username.encode('utf-8')).decode('utf-8')
        return jsonify({'token': token})
    elif not username and token:
        token = token.encode("utf-8")
        try:
            username = encoder.decrypt(token).decode('utf-8')
        except:
            return jsonify({})
        return jsonify({'username': username})
    return jsonify({})


if __name__ == "__main__":
    app.run(host="localhost", port=5557, debug=True, threaded=True)

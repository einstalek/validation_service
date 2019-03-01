from flask import request, jsonify
from functools import wraps
from service import app, allowed_ips, encoder


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


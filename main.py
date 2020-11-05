# -*- coding: utf-8 -*-

import flask


from flask import make_response, render_template


from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = flask.Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash(
        "admin"),
    "ministry": generate_password_hash(
        "ministry")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


@app.route('/<route>')
def render_content(route):
    res = ""
    try:
        res = make_response(render_template('%s/%s' % (route, route)))
        res.headers["Content-Type"] = 'text/plain'
    except:
        pass

    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

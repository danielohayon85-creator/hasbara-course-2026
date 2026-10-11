"""
שרת סטטי קטן לאתר הידע של קורס קציני הסברה 2026, מוגן בסיסמה (HTTP Basic Auth).
משתני סביבה: SITE_USER, SITE_PASS (אם לא מוגדרים - ברירת מחדל למקומי בלבד).
"""
import os
from functools import wraps

from flask import Flask, Response, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)

SITE_USER = os.environ.get("SITE_USER", "kazin")
SITE_PASS = os.environ.get("SITE_PASS", "hasbara2026")


def check_auth(username, password):
    return username == SITE_USER and password == SITE_PASS


def authenticate():
    return Response(
        "גישה מוגבלת - נדרשת הזדהות.", 401,
        {"WWW-Authenticate": 'Basic realm="hasbara-2026"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/")
@requires_auth
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
@requires_auth
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)), debug=True)

"""
שרת סטטי קטן לאתר הידע של קורס קציני הסברה 2026.
"""
import os

from flask import Flask, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)), debug=True)

from flask import Flask, redirect, url_for, jsonify, request, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/photoDb"
mongo = PyMongo(app)

@app.route("/")
def get_initial_response():
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    resp = jsonify(message)
    return resp

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/uploads/<path:filename>", methods=["POST"])
def save_upload(filename):
    mongo.save_file(filename, request.files["image"])
    return redirect(url_for("get_upload", filename=filename))

@app.route("/uploads/<path:filename>")
def get_upload(filename):
    return mongo.send_file(filename)



@app.errorhandler(404)
def page_not_found(e):
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run()

from flask import Flask, Response, redirect, render_template, request, url_for
from database import db
import os

import helper

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
    dbuser=os.environ["DBUSER"],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)
db.init_app(app)
app.app_context().push()
db.create_all()


@app.route("/getCSV")
def get_csv():
    return Response(
        helper.get_csv(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=zu-bbbearbeiten.csv"},
    )


@app.route("/")
def index():
    items = helper.get_all(sorted=True)
    return render_template("index.html", items=items)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text")
    date = request.form.get("deadline")
    category = request.form.get("category")
    description = request.form.get("description")
    helper.add(text, date=date, category=category, description=description)
    return redirect(url_for("index"))


@app.route("/update/<int:index>")
def update(index):
    helper.update(index)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")

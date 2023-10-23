import datetime
import io
import csv
from flask_sqlalchemy import SQLAlchemy
from database import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    date = db.Column(db.DateTime)
    category = db.Column(db.String)
    description = db.Column(db.String)
    isCompleted = db.Column(db.Boolean, default=False)


def get_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Titel", "Datum", "Kategorie", "Beschreibung", "Erledigt?"])
    for item in Item.query.all():
        writer.writerow(
            [
                item.text,
                item.date.strftime("%d.%m.%Y"),
                item.category,
                item.description,
                "x" if item.isCompleted else "o",
            ]
        )
    return output.getvalue()


def oneWeekFromToday():
    today = datetime.datetime.now()
    oneWeek = datetime.timedelta(weeks=1)
    return today + oneWeek


def add(text, date=None, category=None, description=None):
    text = text.replace("b", "bbb").replace("B", "Bbb")
    if date is None:
        date = oneWeekFromToday()
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

    if category is None:
        category = "default"

    if description is None:
        description = ""

    item = Item(text=text, date=date, category=category, description=description)
    db.session.add(item)
    db.session.commit()


def get_all(sorted=False):
    if sorted:
        return [item for item in Item.query.order_by(Item.date.asc(), Item.category.desc())]
    else:
        return Item.query.all()


def get(id):
    return Item.query.get(id)


def update(id):
    item = db.session.query(Item).get(id)
    isCompleted = db.session.query(Item).get(id).isCompleted
    print(item, isCompleted)
    db.session.query(Item).filter(Item.id == id).update(
        {Item.isCompleted: not isCompleted}
    )
    db.session.commit()

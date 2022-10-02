from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random as rnd
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {col.name:getattr(self,col.name) for col in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random():
    cafe=Cafe.query.get(rnd.randint(0,Cafe.query.count()-1))

    return cafe.to_dict()


@app.route("/all")
def all():
    cafes = Cafe.query.all()
    return {"cafes": [cafe.to_dict() for cafe in cafes]}

@app.route("/search")
def search():
    loc= request.args.get("loc")

    cafe = Cafe.query.filter_by(location=loc).first()
    print(loc,cafe)
    if cafe!=None:
        return cafe.to_dict()
    else:
        return jsonify(error="no cafe found near")



@app.route("/add" ,methods=["POST","GET"])
def add():
    newcafe = Cafe(
                name = request.form.get("name"),
                map_url =request.form.get("map_url") ,
                img_url = request.form.get("img_url"),
                location = request.form.get("location"),
                seats = request.form.get("seats"),
                has_toilet =bool(request.form.get("has_toilet")),
                has_wifi = bool(request.form.get("has_wifi")),
                has_sockets = bool(request.form.get("has_sockets")),
                can_take_calls = bool(request.form.get("can_take_calls")),
                coffee_price =request.form.get("coffee_price"))
    db.session.add(newcafe)
    db.session.commit()
    print(request.form.get("name"))
    return {"response":"cafe added successfully"}

@app.route("/update-price/<int:cafeid>", methods=["POST","GET","PATCH"])
def update_price(cafeid):
    newprice=request.form.get("price")


    cafe = Cafe.query.get(cafeid)
    if cafe!=None:
        cafe.coffee_price=newprice
        db.session.commit()
        return {"success": "cafe price updated complete"}
    else:
        return jsonify(error = "cafe not found"),404


@app.route("/delete/<int:cafeid>", methods=["DELETE"])
def delete(cafeid):
    apikey=request.form.get("api-key")

    if apikey=="kedar":
        cafe = Cafe.query.get(cafeid)
        db.session.delete(cafe)
        db.session.commit()
        return {"success": "cafe deleted successfully"}
    else:
        return jsonify(error = "wroung api-key"),404
## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)

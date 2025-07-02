#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        response = [r.to_dict_basic() for r in restaurants]
        return make_response(jsonify(response), 200)


class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return make_response(restaurant.to_dict(), 200)
        return make_response({"error": "Restaurant not found"}, 404)

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        return make_response({"error": "Restaurant not found"}, 404)


class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        response = [p.to_dict_basic() for p in pizzas]
        return make_response(jsonify(response), 200)

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        price = data.get("price")
        if not isinstance(price, int) or not (1 <= price <= 30):
            return make_response({"errors": ["validation errors"]}, 400)

        new_resturant_pizza = RestaurantPizza(
            price=price,
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )
        db.session.add(new_resturant_pizza)
        db.session.commit()

        return make_response(new_resturant_pizza.to_dict(), 201)


api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantById, "/restaurants/<int:id>")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5555, debug=True)


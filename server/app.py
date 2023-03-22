#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/vendors', methods=['GET'])
def vendors():
    vendor_list = [ vendor.to_dict()for vendor in Vendor.query.all()]
    response = make_response(
        jsonify(vendor_list),
        200
    )
    return response

@app.route('/vendors/<int:id>', methods=['GET'])
def vendor_by_id(id):
    vendor = Vendor.query.filter(Vendor.id == id).first()

    if not vendor:
        response_dict = {"error": "Vendor not found"}

        response = make_response(
              jsonify(response_dict),
            404)
        return response

    if request.method == 'GET':
        response = make_response(
            jsonify(vendor.to_dict()),
            200
        )
        return response


@app.route('/sweets')
def sweets():
    sweets_list = [ sweet.to_dict()for sweet in Sweet.query.all()]
    response = make_response(
        jsonify(sweets_list),
        200
    )
    return response

@app.route('/sweets/<int:id>', methods=['GET'])
def sweet_by_id(id):
    sweet = Sweet.query.filter(Sweet.id == id).first()

    if not sweet:
        response_dict = {"error": "Sweet not found"}

        response = make_response(
              jsonify(response_dict),
            404)
        return response

    if request.method == 'GET':
        response = make_response(
            jsonify(sweet.to_dict()),
            200
        )
        return response


@app.route('/vendor_sweets' , methods=['POST'])
def vendor_sweets():
    request_json = request.get_json()

    new_vendor_sweet = VendorSweet(
        price=request_json.get('price'),
        vendor_id=request_json.get('vendor_id'),
        sweet_id=request_json.get('sweet_id')
    )
    db.session.add(new_vendor_sweet)
    db.session.commit()

    if not new_vendor_sweet:
        response_dict = {"error": "Sweet not found"}

        response = make_response(
              jsonify(response_dict),
            404)
        return response
    # vendor=new_vendor_sweet.vendors
    else:
        response = make_response(
            jsonify(new_vendor_sweet.to_dict())
            ,200)

    return response



@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def vendor_sweet_by_id(id):
    vendor_sweet = VendorSweet.query.filter(VendorSweet.id == id).first()
    if not vendor_sweet:
        response_dict = {"error": "VendorSweet not found"}

        response = make_response(
              jsonify(response_dict),
            404)
        return response

    elif request.method == 'DELETE':
        db.session.delete(vendor_sweet)
        db.session.commit()

        response = make_response(
           jsonify({},200)
        )

        return response



if __name__ == '__main__':
    app.run(port=5555)

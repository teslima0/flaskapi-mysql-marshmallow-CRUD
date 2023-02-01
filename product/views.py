from flask import Flask, request,Blueprint,make_response,jsonify
from .models import Product,product_schema,products_schema,UserSchema, User,DriverRating
from flask_jwt_extended import jwt_required,get_jwt_identity,verify_jwt_in_request

views=Blueprint('views',__name__)
deletes=Blueprint('deletes',__name__)
patch=Blueprint('patch',__name__)
from . import db

#status code eeror
@views.errorhandler(404)
def handle_404_error(_error):
    """Return a 404 http status code"""
    return make_response(jsonify({'error': 'page not found'}),404)


@views.errorhandler(500)
def handle_500_error(_error):
    """Return a 500 http status code"""
    return make_response(jsonify({'error': 'internal server error'}),500)


@views.errorhandler(400)
def handle_400_error(_error):
    """Return a 400 http to client"""
    return make_response(jsonify({'error': 'Bad request'}),400)


@views.errorhandler(401)
def handle_401_error(_error):
    """Return a 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorized page'}),401)




@views.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id['id']).first()
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    
    new_product = Product(name, description, price, qty, user)
    
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product)



@views.route('/products', methods = ['GET'])
@jwt_required()
def get_all_product():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id['id'])
    get_products = Product.query.filter_by(user=user).all()
    product_schema = products_schema
    products = product_schema.dump(get_products)
    return make_response(jsonify({"product": products}))


@views.route('/admin', methods = ['GET'])
@jwt_required()
def get_all_product_admin():
    get_jwt_identity()
    get_products = Product.query.all()
    product_schema = products_schema
    products = product_schema.dump(get_products)
    
    return make_response(jsonify({"product": products}))


"""
@views.route('/products/<id>', methods = ['PUT'])
@jwt_required()
def update_product_by_id(id):
    current_user = get_jwt_identity()
    data = request.get_json()
    get_product = Product.query.get_or_404(int(id))
    if data.get('name'):
        get_product.name = data['name']
    if data.get('description'):
        get_product.description = data['description']
    if data.get('price'):
        get_product.price = data['price']
    if data.get('qty'):
        get_product.qty= data['qty']    
    
    db.session.commit()
    
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))

"""
@views.route('/products/<id>', methods=['PUT'])
@jwt_required()
def update_product_by_id(id):
    current_user = get_jwt_identity()
    data = request.get_json()
    get_product = Product.query.get_or_404(int(id))

    if get_product.user_id != current_user['id']:
        return make_response(jsonify({'error': 'You are not authorized to update this product'}), 401)

    if data.get('name'):
        get_product.name = data['name']
    if data.get('description'):
        get_product.description = data['description']
    if data.get('price'):
        get_product.price = data['price']
    if data.get('qty'):
        get_product.qty = data['qty']

    db.session.commit()

    product = product_schema.dump(get_product)
    return make_response(jsonify({'product': product}))


@views.route('/products/<id>', methods=["GET"])
@jwt_required()
def get_product(id):  
    current_user = get_jwt_identity()
    get_product = Product.query.get_or_404(int(id))
    
    return product_schema.jsonify(get_product)

@patch.route("/products/<int:id>", methods=["PATCH"])
@jwt_required
def update_product(id): 
    current_user = get_jwt_identity()
    #data = request.get_json()
    get_product = Product.query.get_or_404(int(id))
    product = Product.query.filter_by(name="product_name").first()
    
    if get_product.user_id != current_user['id']:
        return make_response(jsonify({'error': 'You are not authorized to update this product'}), 401)
    
   
    if not product:
        return jsonify({"message":"product not found"})
    
    name = request.json.get("name")   
    description = request.json.get("description")   
    
    product = Product.query.get_or_404(int(id))  
    
    product.name = name
    product.description = description
    
    db.session.commit()   
    return product_schema.jsonify(product)


@deletes.route("/product/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product_by_user(id):
    current_user = get_jwt_identity()
    get_product = Product.query.get_or_404(int(id))

    # Check if the product was created by the current user
    if get_product.user_id != current_user['id']:
        return jsonify({"message": "You are not authorized to delete this product"}), 401

    db.session.delete(get_product)    
    db.session.commit()    
    return product_schema.jsonify(get_product)



@views.route('/products', methods=['GET'])
@jwt_required
def get_products_for_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    products = Product.query.filter_by(user_id=user.id).all()
    return products_schema.jsonify(products)


@views.route("/driverrating", methods=["POST"])
def add_driver_rating():
    data = request.get_json()
    rating_count = data["rating_count"]
    rating_comment = data["rating_comment"]
    history_id = data["history_id"]
    driver_id = data["driver_id"]
    
    new_driver_rating = DriverRating(
        rating_count=rating_count, 
        rating_comment=rating_comment,
        history_id=history_id,
        driver_id=driver_id
    )
    
    db.session.add(new_driver_rating)
    db.session.commit()
    
    return jsonify({"message": "Driver rating added successfully"})

@views.route("/driverrating/<rating_id>", methods=["GET"])
def get_driver_rating(rating_id):
    driver_rating = DriverRating.query.get_or_404(rating_id)
    
    if driver_rating is None:
        return jsonify({"message": "Driver rating not found"}), 404
    
    return jsonify({
        "id": driver_rating.id,
        "rating_count": driver_rating.rating_count,
        "rating_comment": driver_rating.rating_comment,
        "date_added": driver_rating.date_added,
        "history_id": driver_rating.history_id,
        "driver_id": driver_rating.driver_id
    })


'''
@views.route("/register", methods=["POST"])
def register():
    user_schema = UserSchema()
    user_data = request.get_json()

    errors = user_schema.validate(user_data)

    if errors:
        return {"message": "Validation errors", "errors": errors}, 400

    new_user = User(username=user_data["username"], email=user_data["email"], password=user_data["password"])
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully."}, 201




'''


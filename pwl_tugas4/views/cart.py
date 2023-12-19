from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from sqlalchemy.orm import Session
from ..models import Cart

@view_config(route_name='carts', request_method='POST', renderer='json')
def create_cart(request):
    """ Create a new cart record in the database. """
    db = request.dbsession
    data = request.json_body

    # Validate input data
    if not all(key in data for key in ('user_id', 'product_id', 'quantity')):
        raise HTTPBadRequest('Missing required fields')

    # Create a new Cart object with the input values
    cart = Cart(user_id=data['user_id'], product_id=data['product_id'], quantity=data['quantity'])

    # Add the new cart to the database
    db.add(cart)
    db.flush()

    # Return the newly created cart as JSON
    return cart.to_dict()

@view_config(route_name='carts', request_method='GET', renderer='json')
def get_carts(request):
    """ Retrieve a list of cart records from the database. """
    db = request.dbsession
    skip = request.params.get('skip', 0)
    limit = request.params.get('limit', 100)

    # Retrieve a list of carts from the database
    carts = db.query(Cart).offset(skip).limit(limit).all()

    # Return the list of carts as JSON
    return [cart.to_dict() for cart in carts]

@view_config(route_name='cart', request_method='GET', renderer='json')
def get_cart(request):
    """ Retrieve a cart record from the database by ID. """
    db = request.dbsession
    cart_id = request.matchdict['id']

    # Retrieve the cart from the database
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    # Return the cart as JSON, or raise a 404 error if it doesn't exist
    if cart is not None:
        return cart.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='cart', request_method='PUT', renderer='json')
def update_cart(request):
    """ Update an existing cart record in the database. """
    db = request.dbsession
    cart_id = request.matchdict['id']
    data = request.json_body

    # Retrieve the cart from the database
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    # Update the cart with the input values
    if cart is not None:
        if 'user_id' in data:
            cart.user_id = data['user_id']
        if 'product_id' in data:
            cart.product_id = data['product_id']
        if 'quantity' in data:
            cart.quantity = data['quantity']

        # Commit the changes to the database
        db.commit()

        # Return the updated cart as JSON
        return cart.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='cart', request_method='DELETE', renderer='json')
def delete_cart(request):
    """ Delete a cart record from the database by ID. """
    db = request.dbsession
    cart_id = request.matchdict['id']

    # Retrieve the cart from the database
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    # Delete the cart from the database
    if cart is not None:
        db.delete(cart)
        db.commit()

        # Return a success message as JSON
        return {'message': 'Cart deleted'}
    else:
        raise HTTPNotFound()
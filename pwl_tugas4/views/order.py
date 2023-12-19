from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from sqlalchemy.orm import Session
from ..models import Order

@view_config(route_name='orders', request_method='POST', renderer='json')
def create_order(request):
    """ Create a new order record in the database. """
    db = request.dbsession
    data = request.json_body

    # Validate input data
    if not all(key in data for key in ('user_id', 'product_id', 'quantity')):
        raise HTTPBadRequest('Missing required fields')

    # Create a new Order object with the input values
    order = Order(user_id=data['user_id'], product_id=data['product_id'], quantity=data['quantity'])

    # Add the new order to the database
    db.add(order)
    db.flush()

    # Return the newly created order as JSON
    return order.to_dict()

@view_config(route_name='orders', request_method='GET', renderer='json')
def get_orders(request):
    """ Retrieve a list of order records from the database. """
    db = request.dbsession
    skip = request.params.get('skip', 0)
    limit = request.params.get('limit', 100)

    # Retrieve a list of orders from the database
    orders = db.query(Order).offset(skip).limit(limit).all()

    # Return the list of orders as JSON
    return [order.to_dict() for order in orders]

@view_config(route_name='order', request_method='GET', renderer='json')
def get_order(request):
    """ Retrieve an order record from the database by ID. """
    db = request.dbsession
    order_id = request.matchdict['id']

    # Retrieve the order from the database
    order = db.query(Order).filter(Order.id == order_id).first()

    # Return the order as JSON, or raise a 404 error if it doesn't exist
    if order is not None:
        return order.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='order', request_method='PUT', renderer='json')
def update_order(request):
    """ Update an existing order record in the database. """
    db = request.dbsession
    order_id = request.matchdict['id']
    data = request.json_body

    # Retrieve the order from the database
    order = db.query(Order).filter(Order.id == order_id).first()

    # Update the order with the input values
    if order is not None:
        if 'user_id' in data:
            order.user_id = data['user_id']
        if 'product_id' in data:
            order.product_id = data['product_id']
        if 'quantity' in data:
            order.quantity = data['quantity']

        # Commit the changes to the database
        db.commit()

        # Return the updated order as JSON
        return order.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='order', request_method='DELETE', renderer='json')
def delete_order(request):
    """ Delete an order record from the database by ID. """
    db = request.dbsession
    order_id = request.matchdict['id']

    # Retrieve the order from the database
    order = db.query(Order).filter(Order.id == order_id).first()

    # Delete the order from the database
    if order is not None:
        db.delete(order)
        db.commit()

        # Return a success message as JSON
        return {'message': 'Order deleted'}
    else:
        raise HTTPNotFound()
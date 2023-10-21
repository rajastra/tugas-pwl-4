from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from .. import models

@view_config(route_name='list', renderer='json')
def list_view(request):
    try:
        all = {
            'data': [
                {'id': 1, 'name': 'one'},
                {'id': 2, 'name': 'two'},
                {'id': 3, 'name': 'three'},
            ]
        }
    except SQLAlchemyError:
        return Response("Pyramid is having a problem using your SQL database.  The problem", content_type='text/plain', status=500)
    return all

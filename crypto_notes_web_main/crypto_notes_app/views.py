from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='hello', renderer='templates/hello.pt')
def hello_world(request):
    return {'content': 'Hello World!'}

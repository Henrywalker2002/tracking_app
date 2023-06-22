import uuid 
import logging

from threading import local

_user = local()

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        id = uuid.uuid4()
        logging.info("{} start".format(id))
        request.content_params.update({"id" : id})
        # assign for created_by or updated_by
        _user.__setattr__('value', request.user)
        response = self.get_response(request)
        
        logging.info("{} end".format(id))
        return response


def get_current_user():
    return _user.value 
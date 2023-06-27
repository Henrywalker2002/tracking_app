import uuid 
import logging

logging.basicConfig(filename= "log.txt", level= logging.INFO)

from threading import local

_user = local()

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user : 
            _user.__setattr__('user', request.user)
            
        # id for debug logger
        id = uuid.uuid4()
        _user.__setattr__('request_id' , id)
        logging.info(f'request id {str(id)} start method {request.method} path {request.get_full_path()} body {request.body}')
        response = self.get_response(request)
        logging.info(f'request id {str(id)} end request\n')
        return response

def get_current_user():
    """
    get request.user to save in model 
    """
    return _user.user 

def get_current_request_id():
    return _user.request_id
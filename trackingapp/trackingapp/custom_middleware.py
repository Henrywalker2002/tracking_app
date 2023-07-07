import uuid
import logging
import threading
import functools

logging.basicConfig(filename="log.txt", level=logging.INFO)

_user = threading.local()

class CustomMiddleware:
    """
    Add request id and request.user to local
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user:
            _user.__setattr__('user', request.user)

        # id for debug logger
        id = uuid.uuid4()
        _user.__setattr__('request_id', id)
        logging.info(
            f'request id {str(id)} start request with method {request.method} path {request.get_full_path()} body {request.body}')
        response = self.get_response(request)
        logging.info(f'request id {str(id)} end request\n')
        return response


def get_current_user():
    """
    get request.user to save in model 
    """
    return getattr(_user, 'user', None)


def get_current_request_id():
    return getattr(_user, "request_id", None)


class CustomThread(threading.Thread):
    """
    Custom thread to save request.user and request id when create new thread
    """

    def start(self):
        self.user = get_current_user()
        self.request_id = get_current_request_id()
        super().start()

    def run(self):
        global _user
        if not hasattr(_user, 'user'):
            setattr(_user, 'user', self.user)
        if not hasattr(_user, 'request_id'):
            setattr(_user, 'request_id', self.request_id)
        super().run()

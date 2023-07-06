import uuid
import logging
import threading
import functools

from queue import Queue

taskQueue = Queue()
lock = threading.Lock()

logging.basicConfig(filename="log.txt", level=logging.INFO)

_user = threading.local()


def add_to_queue(func):
    global taskQueue, lock
    
    @functools.wraps(func)
    def inner(*args, **kwargs):
        lock.acquire()
        taskQueue.put((func, args, kwargs))
        lock.release()
    return inner
    

def proccess_task_queue():
    """
    element is tuple (func_name, args, kwargs)
    """
    global taskQueue
    lock.acquire()
    ele = taskQueue.get()
    lock.release()
    ele[0](*ele[1], **ele[2])
    proccess_task_queue()

class CustomMiddleware:
    """
    Add request id and request.user to local
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        thread_process_task = threading.Thread(target= proccess_task_queue, args=(), daemon= True)
        thread_process_task.start()
        
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
    return _user.request_id


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

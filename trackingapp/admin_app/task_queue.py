from queue import Queue
from trackingapp.custom_middleware import CustomThread
import threading
import functools

taskQueue = Queue()
lock = threading.RLock()

def add_to_queue(func):
    """
    decorator to add task into task queue 
    """
    global taskQueue, lock
    
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # lock.acquire()
        taskQueue.put((func, args, kwargs))
        # lock.release()
    return inner
    

def proccess_task_queue():
    """
    element is tuple (func_name, args, kwargs)
    """
    global taskQueue, lock
    lock.acquire()
    ele = taskQueue.get()
    lock.release()
    ele[0](*ele[1], **ele[2])
    proccess_task_queue()
    

from queue import Queue
from trackingapp.custom_middleware import CustomThread
import threading
import functools

taskQueue = Queue()

def add_to_queue(func):
    """
    decorator to add task into task queue 
    """
    global taskQueue
    
    @functools.wraps(func)
    def inner(*args, **kwargs):
        taskQueue.put((func, args, kwargs))
    return inner
    

def proccess_task_queue():
    """
    element is tuple (func_name, args, kwargs)
    """
    global taskQueue
    ele = taskQueue.get()
    ele[0](*ele[1], **ele[2])
    proccess_task_queue()
    

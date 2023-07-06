from django.db import connection, reset_queries
import functools
import time
from trackingapp.custom_middleware import get_current_request_id 
import logging
import inspect

def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        logging.info("Function : " + func.__name__)
        logging.info("Number of Queries : {}".format(end_queries - start_queries))
        logging.info("Finished in : {}".format(end - start))

        return result

    return inner_func

def log_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kawrgs):
        id = get_current_request_id()
        logging.info(f'request {id} begin to {func.__name__} param {args} {kawrgs}')
        result = func(*args, **kawrgs)
        logging.info(f'request {id} end {func.__name__}')
        return result
    
    return inner_func
        
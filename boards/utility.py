from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        for query in connection.queries:
            print("SQl = {}".format(query['sql']))
        return result

    return inner_func


def get_pagination(queryset, page, items):
    paginator = Paginator(queryset, items)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        items = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        items = paginator.page(paginator.num_pages)

    return items

from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100 # Default number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 1000 # Maximum number of results per page

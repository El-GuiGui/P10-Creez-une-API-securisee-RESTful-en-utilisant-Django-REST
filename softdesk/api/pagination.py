from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination standard pour les résultats de l'API.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

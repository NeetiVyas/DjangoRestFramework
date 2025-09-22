from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'   #/api/items?page_size=10
    page_query_param = 'page-num'   #/api/items?page-num=3
    max_page_size = 5   #limits the maximum number of items that a client can request per page

    #allows client to dynamically select page size and page-num

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })
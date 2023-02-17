from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'items_per_page'
    max_page_size = 50
    page_query_param = 'page'
    def get_paginated_response(self, data):
        return Response({
            'next_page_url': self.get_next_link(),
            'prev_page_url': self.get_previous_link(),
            'page': self.page.number,
            'count': self.page.paginator.count,
            'items_per_page': self.page_size,
            'data': data,
        })
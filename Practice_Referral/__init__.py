from __future__ import absolute_import
from .celery import app as celery_app
from rest_framework import pagination
from rest_framework.views import exception_handler
from rest_framework import exceptions
from django.http.response import REASON_PHRASES
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    ''' Custom Pagination to be used in rest api'''

    def get_paginated_response(self, data):
        ''' override pagination structure in list rest api '''

        next_page = self.page.next_page_number() if \
            self.page.has_next() else None
        previous_page = self.page.previous_page_number() if \
            self.page.has_previous() else None
        return Response({
            'pagination': {
                'next_url': self.get_next_link(),
                'previous_url': self.get_previous_link(),
                'current_page': self.page.number,
                'next_page': next_page,
                'previous_page': previous_page,
                'first_page': 1,
                'last_page': self.page.paginator.num_pages,
                'page_size': self.page_size,
                'count': self.page.paginator.count,
            },
            'results': data
        })


def custom_rest_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, exceptions.NotAuthenticated):
        response.status_code = 401
        response.reason_phrase = REASON_PHRASES.get(response.status_code)
    return response

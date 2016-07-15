from __future__ import absolute_import
from .celery import app as celery_app
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.views import exception_handler
from rest_framework import exceptions
from django.http.response import REASON_PHRASES
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    ''' Custom Pagination to be used in rest api'''

    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_page_size(self, request):
        page_size = self.page_size
        if self.page_size_query_param:
            try:
                page_size = _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=False,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass
        if page_size == 0:
            page_size = self.max_page_size
        return page_size

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
                'page_size': self.get_page_size(self.request),
                'count': self.page.paginator.count,
            },
            'results': data
        })


def custom_rest_exception_handler(exc, context):
    ''' Custom rest api exception handler '''
    response = exception_handler(exc, context)
    if isinstance(exc, exceptions.NotAuthenticated):
        response.status_code = 401
        response.reason_phrase = REASON_PHRASES.get(response.status_code)
    if isinstance(exc, exceptions.ValidationError) and \
            'already exists' in str(exc):
        response.status_code = 409
        response.reason_phrase = REASON_PHRASES.get(response.status_code)

    return response


class PaginationPageSizeMixin(object):
    '''
    a mixin class to be used in rest viewset.
    by extending this class you can customize page_size by setting
    'max_page_size' property in class.
    if max_page_size = 0, this mean this support infinite page_size.
    then user can have a query on list rest api by page_size=0.
    '''
    BIG_PAGE_SIZE = 10000000

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        paginator = super().paginator
        max_page_size = getattr(self, 'max_page_size', paginator.max_page_size)

        paginator.max_page_size = max_page_size or self.BIG_PAGE_SIZE
        return paginator


class DynamicFieldsSerializerMixin(object):
    '''
    This class allow you to have dynamic fields in get rest api.
    user can pass "fields" and "xfields" as a get query parameter.
    "fields" specify list of fields you want to be shown as a result.
    "xfields" specify list of fields you want to be excluded in result.
    i.e:
    fields=id,name
    or
    xfields=name1,name2
    '''
    def __init__(self, *args, **kwargs):
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)
        if not self.context:
            return

        params = self.context['request'].query_params
        fields = params.get('fields')
        xfields = params.get('xfields')
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif xfields:
            xfields = xfields.split(',')
            for field_name in xfields:
                self.fields.pop(field_name, None)

"""Пагинация для привычек"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class HabitPagination(PageNumberPagination):
    """Пагинатор для списка привычек"""

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Кастомный формат ответа с пагинацией"""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page_info': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.page_size,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            }
        })

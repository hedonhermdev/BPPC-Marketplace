from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size = 2
    cursor_query_param = "cursor"
    ordering = "-created"
    template = None

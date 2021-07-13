from rest_framework.pagination import PageNumberPagination

from sgd.constants import TRUE_OPTIONS


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    paginated_query_param = 'paginated'

    def get_default_pagination_value(self, view):
        if view is not None and hasattr(view, 'paginated'):
            return view.paginated
        return True

    def paginate_queryset(self, queryset, request, view=None):
        paginated = request.GET.get(
            self.paginated_query_param,
            self.get_default_pagination_value(view))
        if paginated in TRUE_OPTIONS:
            return super().paginate_queryset(queryset, request, view)
        return None

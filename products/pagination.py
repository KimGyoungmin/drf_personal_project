from rest_framework.pagination import PageNumberPagination

## 페이지네이션 커스텀
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
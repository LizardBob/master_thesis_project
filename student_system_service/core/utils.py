from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet


def get_paginator(qs: QuerySet, page_size: int, page: int, paginated_type, **kwargs):
    paginator = Paginator(qs, page_size)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return paginated_type(
        page=page_obj.number,
        pages=paginator.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )

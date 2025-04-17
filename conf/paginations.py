from math import ceil
from typing import Union, Dict


class Pagination:
    def __init__(self, page, limit, total_count, data):
        self._total_pages = ceil(total_count/limit)
        self._page = page
        self._count = total_count
        self._page_size = limit
        self.data = data

    @property
    def _next(self) -> Union[int, object]:
        """
        Calculating the next page for pagination
        returns int() or None
        """
        if int(self._total_pages) - int(self._page) > 0:
            return self._page + 1
        return

    @property
    def _previous(self) -> Union[int, object]:
        """
        Calculating the previous page for pagination
        returns int() or None
        """
        if int(self._total_pages) - int(self._page) >= 0 and int(self._page) - 1 > 0:
            return int(self._page) - 1
        return None

    def generate_pagination(self) -> Dict:
        """
        Generating the pagination data
        return dictionary object
        results (data) will be updated from the view
        """
        data = dict(
            totalCount=self._count,
            page=self._page,
            limit=self._page_size,
            nextPage=self._next,
            prevPage=self._previous,
        )
        return data

    def get_paginated_data(self) -> Dict:
        """
        Generating the pagination data
        return dictionary object
        results (data) will be updated from the view
        """
        data = dict(
            totalCount=self._count,
            page=self._page,
            limit=self._page_size,
            nextPage=self._next,
            prevPage=self._previous,
            pageCount=self._total_pages,
            data=self.data
        )
        return data

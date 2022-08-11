from app.api.deps.user import get_user_manager

from typing import Union

from fastapi import Query


class PaginateQueryParams:
    """dependency for pagination"""

    def __init__(
            self,
            page: int = Query(1, description="page number"),
            page_size: Union[None, int] = Query(
                None,
                description="maximum of items per page. Default to settings.DEFAULT_PAGE_SIZE",
            ),
    ) -> None:
        self.page = page
        self.page_size = page_size
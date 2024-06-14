from typing import Annotated

from fastapi import Query


async def page_data(
    page_size: Annotated[
        int, Query(
            title='Pagination page size',
            description='Размер страницы для пагинации',
            gt=0,
            lt=100,
        ),
    ] = 50,
    page_number: Annotated[
        int, Query(
            title='Pagination page number',
            description='Номер страницы для пагинации',
            ge=0,
        ),
    ] = 0,
):
    return {'page_size': page_size, 'page_number': page_number}

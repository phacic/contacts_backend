from typing import Union

import strawberry


@strawberry.type
class Error:
    err_text: Union[None, str]
    code: Union[None, int]
    description: Union[None, str]

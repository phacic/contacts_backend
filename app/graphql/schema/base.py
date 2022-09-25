from typing import Union

import strawberry

from app.internal import BaseError


@strawberry.type
class Error(BaseError):
    code: int

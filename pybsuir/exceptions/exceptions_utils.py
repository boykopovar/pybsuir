from typing import Any

from pybsuir.exceptions import BsuirStatsException


def create_api_exception(status: int,
                         url: str,
                         text: str,
                         headers: dict,
                         other: Any = None) -> BsuirStatsException:

    return BsuirStatsException(
        status=status,
        url=url,
        text=text,
        headers=headers
    )
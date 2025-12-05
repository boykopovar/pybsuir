import json
import re
from typing import Optional


class BsuirStatsException(Exception):
    def __init__(self, status: int, url: str, text: str, headers: dict):
        self.status = status
        self.url = url
        self.text = text
        self.headers = headers
        super().__init__(self.full_error())

    def full_error(self):
        return (
            f"API Error: {self.status}\n"
            f"URL: {self.url}\n"
            f"Response Text: {self.text}\n"
            f"Headers: {json.dumps(dict(self.headers), indent=2)}"
        )

    def __str__(self):
        msg = getattr(self, "message", getattr(self, "text", None))
        return f"{msg}" if msg else f"{self.status}"

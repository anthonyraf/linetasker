from datetime import datetime
from typing import Any
from collections.abc import Iterable


class Filter:
    """Describe a filter object to be passed to list_tasks function"""

    def __init__(
        self,
        tags: Iterable[str] | None = None,
        priority: int | None = None,
        date: datetime | None = None,
    ):
        self.tags = tags
        self.priority = priority
        self.date = date

    def is_valid(self, task: dict[str, Any]) -> bool:
        """Check if the task passed in argument is following the filter
        requirements"""
        validity = True
        for tag in self.tags:
            if tag not in task["tags"]:
                validity = False

        return validity

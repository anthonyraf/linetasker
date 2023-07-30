from typing import NamedTuple
from datetime import datetime
from dataclasses import dataclass, field, asdict


class DateTime(NamedTuple):
    date: str
    time: str


DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class Status:
    ACTIVE: str = "active"
    DONE: str = "done"
    DELETED: str = "deleted"
    UNDEFINED: str = "undefined"


@dataclass
class Task:
    id: int
    description: str
    priority: int
    status: str = field(default=Status.ACTIVE)
    created: NamedTuple = DateTime(
        date=datetime.now().strftime(DATE_FORMAT),
        time=datetime.now().strftime(TIME_FORMAT),
    )
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

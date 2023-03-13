from dataclasses import dataclass
from hashlib import sha256


class Task:
    def __init__(self, task: str, priority: int) -> None:
        self.id = None
        self.task = task
        self.priority = priority
        self.hash = None
        self.short_hash = None

    @staticmethod
    def generate_hash(data: str) -> str:
        return sha256(data.encode("utf-8")).hexdigest()


import os
import json
from typing import Any
from rich.console import Console
from pathlib import Path
from contextlib import contextmanager

from .task import Task, Status
from .utils.prettier import TaskTemplate, TaskList


import logging
import coloredlogs

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s : %(message)s"
)

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


CURRENT_DIR = Path(__file__).parent
console = Console()


class Register:
    def __init__(self, filename):
        self.filename = filename
        self.db = ConfigFile(self.filename, CURRENT_DIR)
        self.db.create_file()
        self.db_dict: dict[str, Any] = self.db.read()

    @property
    def cursor(self):
        return self.db_dict["cursor"]

    @property
    def unique_key(self):
        return self.db_dict["cumul_count"]

    @cursor.setter
    def cursor(self, value):
        self.db_dict["cursor"] = value

    @unique_key.setter
    def unique_key(self, value):
        """Key that contains the numbers of added task and
        never change even if a task is deleted"""
        self.db_dict["cumul_count"] = value

    @contextmanager
    def update_db(self):
        try:
            yield
        finally:
            self.db.write(self.db_dict)

    def create_task(self, description, priority):
        """Create new task in the database"""
        with self.update_db():
            id = self.cursor

            new_task = Task(id, description, priority)

            self.db_dict["tasks"].append(ntd := new_task.__dict__)
            logging.debug(f"Added: {ntd}")

            self.cursor += 1
            self.unique_key += 1

    def rearange_id(self) -> None:
        with self.update_db():
            for i in range(self.cursor):
                self.db_dict["tasks"][i]["id"] = i

    def delete_task(self, *ids, rearange=True) -> None:
        with self.update_db():
            for id in ids:
                if not 0 <= id <= self.cursor - 1:
                    raise IndexError(f"There is no task n°{id}")
                self.db_dict["tasks"].pop(id)
                logging.debug(f"Deleted: {self.db_dict['tasks'][id]}")
                self.cursor -= 1

        if rearange:
            self.rearange_id()

    def done(self, task_id: int) -> None:
        """Mark as done a task by its id."""
        with self.update_db():
            Task.change_field_value(
                self.db_dict, task_id, field="status", value=Status.DONE
            )

    def undone(self, task_id: int) -> None:
        with self.update_db():
            Task.change_field_value(
                self.db_dict, task_id, field="status", value=Status.ACTIVE
            )

    def show(self, task_id: int):
        """Show details about a tasks (creation date, hour, ...)"""
        pass

    def list(self, n=None):
        task_list = TaskList()
        # logging.debug(self.db_dict["tasks"])

        for task in self.db_dict["tasks"]:
            task_list.add_rows(TaskTemplate(**task))

        logging.debug("CALLED: core.Register.list")
        console.print(task_list.render())

    def clean(self) -> None:
        with self.update_db():
            for task in self.db_dict["tasks"]:
                if task["status"] == Status.DONE:
                    self.delete_task(task["id"], rearange=False)
            self.rearange_id()


class ConfigFile:
    """
    Class for handling the json configuration file as database
    """

    def __init__(self, filename: str, abs_path: Path):
        self.filename = (
            filename if filename.endswith(".json") else filename + ".json"
        )

        if abs_path is None:
            self.file_abs_path = CURRENT_DIR / Path(self.filename)
        else:
            self.file_abs_path = abs_path / Path(self.filename)

    def create_file(self):
        """Create the json file and fill out with the default template"""
        default_json = json.dumps(
            {"tasks": [], "cursor": 0, "cumul_count": 0}, indent=4
        )

        if not os.path.exists(self.file_abs_path):
            with open(self.file_abs_path, "w") as file:
                file.write(default_json)
        else:
            with open(self.file_abs_path, "r+") as file:
                if file.read().strip() == "":
                    file.write(default_json)

    def read(self) -> dict[str, Any]:
        with open(self.file_abs_path) as file:
            return json.loads(file.read())

    def write(self, content: dict[str, Any]):
        with open(self.file_abs_path, "w") as file:
            file.write(json.dumps(content, indent=4))

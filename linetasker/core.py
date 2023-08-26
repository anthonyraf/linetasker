import os
import json
from typing import Any
from rich.console import Console
from rich.prompt import Confirm
from pathlib import Path
from contextlib import contextmanager

from linetasker.task import Task, Status
from linetasker.utils.prettier import TaskTemplate, TaskList


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
        return len(self.db_dict["tasks"])

    @cursor.setter
    def cursor(self, value):
        raise Exception("The cursor value cannot be changed")

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

    def rearrange_id(self) -> None:
        with self.update_db():
            for i in range(self.cursor):
                self.db_dict["tasks"][i]["id"] = i

    def delete_task(self, *ids) -> None:
        for id in ids:
            if not 0 <= id <= self.cursor - 1:
                raise IndexError(f"There is no task n°{id}")
        with self.update_db():
            if len(ids) == 1:
                self.db_dict["tasks"].pop(*ids)
            else:
                self.db_dict["tasks"] = [
                    task
                    for pos, task in enumerate(self.db_dict["tasks"])
                    if pos not in ids
                ]
        self.rearrange_id()

    def done(self, task_id: int) -> None:
        """Mark as done a task by its id."""
        with self.update_db():
            self.db_dict["tasks"][task_id]["status"] = Status.DONE

    def undone(self, task_id: int) -> None:
        with self.update_db():
            self.db_dict["tasks"][task_id]["status"] = Status.ACTIVE

    def show(self, task_id: int):
        """Show details about a tasks (creation date, hour, ...)"""
        pass

    def list_tasks(self, n=None):
        task_list = TaskList()

        for task in self.db_dict["tasks"]:
            task_list.add_rows(TaskTemplate(**task))

        logging.debug("CALLED: core.Register.list")
        console.print(task_list.render())

    def get_done_tasks(self) -> list[int]:
        """Return a list of the id of all done tasks"""
        done_tasks = []
        for task in self.db_dict["tasks"]:
            if task["status"] == Status.DONE:
                done_tasks.append(task["id"])
        return done_tasks

    def clean(self) -> None:
        self.delete_task(*self.get_done_tasks())

    def reset(self, bypass_flag: bool) -> None:
        # Confirmation prompt, yes by default
        n_tasks = len(self.db_dict["tasks"])
        if not bypass_flag:
            if not Confirm.ask(
                "Are you sure to delete [red]all[/red] tasks ?"
            ):
                return
        with self.update_db():
            self.db_dict["tasks"] = []
        console.print(f"[green]{n_tasks} tasks deleted successfully ![/green]")


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
        default_json = json.dumps({"tasks": []}, indent=4)

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

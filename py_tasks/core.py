import os
import json
from typing import Any
from rich.console import Console
from pathlib import Path
from contextlib import contextmanager
from .task import Task, Status


CURRENT_DIR = Path(__file__).parent

class Prettier:
    def __init__(self):
        self.console = Console()
        

    def print(self, task: dict):
        """"""
        self.console.rule("[bold magenta]Anthony", style="green")


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

    def create_task(self, task, priority):
        """Create new task in the database"""
        with self.update_db():
            id = self.cursor

            new_task = Task(id, task, priority)
            new_task.set_active()
        
            self.db_dict["tasks"].append(new_task.__dict__)
            self.cursor += 1
            self.unique_key += 1

    def delete_task(self, id):
        """Remove task by its id"""
        with self.update_db():
            if len(self.db_dict["tasks"]) == 0:
                raise IndexError("There is no tasks in the database")

            el_key = None # Flag to indicate from which key to decrement
            for i in range(len(tasks := self.db_dict["tasks"])):
                if el_key is not None:
                    #self.db_dict["tasks"][i]["id"] = i - 1
                    Task.change_field_value(self.db_dict, i,
                                            "id", i - 1)

                if tasks[i]["id"] == id: # tasks[i] is the i-th task
                    el_key = i
            
            if el_key is None:
                raise Exception(f"The task n°{id} doesn't exist")

            self.db_dict["tasks"].pop(el_key)  # Remove task by its key
            self.cursor -= 1  # Update number of active tasks

    def done(self, id_task: int) -> None:
        """Mark as done a task by its id."""
        with self.update_db():
            Task.change_field_value(self.db_dict, id_task,
                                    "status", Status.DONE)


    def undone(self, id_task) -> None:
        with self.update_db():
            Task.change_field_value(self.db_dict, id_task,
                                    "status", Status.ACTIVE)

    def show(self):
        """Show details about a tasks (creation date, hour, ...)"""
        pass

    def list(self, n=None):
        # self.use_db()
        # for task in self.db_dict["tasks"]:
        #     print(task["task"])
        for tasks in self.db_dict["tasks"]:
            print(tasks["task"])

        # p = Prettier()
        # p.print({})



class ConfigFile:
    """
    Class for handling the json configuration file as database
    """

    def __init__(self, filename: str, abs_path: Path):
        self.filename = filename if filename.endswith(".json") else filename + ".json"
        
        if abs_path is None:
            self.file_abs_path = CURRENT_DIR / Path(self.filename)
        else:
            self.file_abs_path = abs_path / Path(self.filename)

    def create_file(self):
        """Create the json file and fill out with the default template"""
        default_json = json.dumps(
            {"tasks": [],
            "cursor": 0,
            "cumul_count": 0},
            indent=4)

        if not os.path.exists(self.file_abs_path):
            with open(self.file_abs_path, 'w') as file:
                file.write(default_json)
        else:
            with open(self.file_abs_path, "r+") as file:
                if file.read().strip() == "":
                    file.write(default_json)

    def read(self) -> dict[str, Any]:
        with open(self.file_abs_path, 'r') as file:
            return json.loads(file.read())

    def write(self, content: dict[str, Any]):
        with open(self.file_abs_path, 'w') as file:
            file.write(json.dumps(content, indent=4))


if __name__ == '__main__':
    r = Register("database")

    r.create_task("kfzjfzfez", 55)

    # logging.debug(pprint.pformat(c.read(), indent=4, sort_dicts=False))

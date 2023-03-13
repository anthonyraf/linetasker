import os
import json
from typing import Any
from task import Task
from dataclasses import dataclass

CURRENT_DIR = os.path.abspath(".")

@dataclass
class Register:
    filename: str

    def __init__(self, filename):
        self.filename = filename
    @property
    def cursor(self):
        return self.db_content["cursor"]

    @cursor.setter
    def cursor(self, value):
        self.db_content["cursor"] = value
    @property
    def unique_key(self):
        return self.db_content["cumul_count"]

    @unique_key.setter
    def unique_key(self, value):
        self.db_content["cumul_count"] = value

    def init_db(self):
        self.db = ConfigFile(self.filename)
        self.db_content = self.db.read()

    def create_task(self, *args, **kwargs):
        """Add new task in the database"""
        new_task = Task(*args, **kwargs)

        new_task.id = self.cursor
        new_task.hash = Task.generate_hash(
            "%s-#%s" % (
                new_task.task,
                self.unique_key,))
        new_task.short_hash = new_task.hash[:5]

        self.db_content["tasks"].append(new_task.__dict__)

        self.cursor += 1
        self.unique_key += 1
        self.update_db()

    def remove_task(self, hash):
        """Remove task by its hash or partial hash"""
        if len(self.db_content["tasks"]) == 0:
            raise IndexError("There is no tasks in the database")

        match = lambda el: el["hash"].startswith(hash)

        el_key = None
        for i in range(len(tasks := self.db_content["tasks"])):
            if el_key is not None:
                self.db_content["tasks"][i]["id"] = i - 1

            if match(tasks[i]):
                el_key = i

        self.db_content["tasks"].pop(el_key)  # Remove task by its key
        self.cursor -= 1  # Update number of active tasks
        self.update_db()

    def mark(self):
        """Mark as done a task by its index or hash.
        TODO: In the cli command, add either mark and done subcommands """
        pass

    def show(self, n=None):
        """List tasks"""
        pass

    def update_db(self):
        """Update database after a change"""
        self.db.write(self.db_content)

    def __call__(self, *args, **kwargs):
        pass


class ConfigFile:
    """
    Class for handling the json configuration file as database
    """

    def __init__(self, filename: str):
        self.filename = filename if filename.endswith(".json") else filename + ".json"
        self.file_abs_path = os.path.join(CURRENT_DIR, self.filename)

        default_json = json.dumps(
            {"tasks": [],
            "cursor": 0,
            "cumul_count": 0},
            indent=4)

        if not os.path.exists(self.file_abs_path):
            with open(self.filename, 'w') as file:
                file.write(default_json)
        else:
            with open(self.filename, "r+") as file:
                if file.read().strip() == "":
                    file.write(default_json)
    def read(self) -> dict[str, Any]:
        with open(self.filename, 'r') as file:
            return json.loads(file.read())

    def write(self, content: dict[str, Any]):
        with open(self.filename, 'w') as file:
            file.write(json.dumps(content, indent=4))


if __name__ == '__main__':
    r = Register("database")

    r.create_task("kfzjfzfez", 55)

    # logging.debug(pprint.pformat(c.read(), indent=4, sort_dicts=False))

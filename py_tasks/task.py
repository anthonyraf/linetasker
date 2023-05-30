from dataclasses import dataclass

class Status:
    ACTIVE: str = 'active'
    DONE: str = 'done'
    DELETED: str = 'deleted'
    UNDEFINED: str = 'undefined'

    @classmethod
    def __getitem__(cls, key):
        key = key.upper()
        return getattr(cls, key)

@dataclass
class Task:
    id: int
    task: str
    priority: int
    status: str = Status.UNDEFINED
    
    def set_active(self):
        self.status = Status.ACTIVE

    @staticmethod
    def change_field_value(db: dict, id_task: int, field: str, value):
        #if id_task - db["cursor"] - 1 < 0:
        if db["cursor"] - 1 < id_task:
            raise IndexError(f"There is no task n°{id_task}")
        
        if field not in {"id" "task", "priority", "status"}:
            raise AttributeError(f"There is no field: {field}")

        db["tasks"][id_task][field] = value


if __name__ == '__main__':
    s = Status()
    print(s['active']) 
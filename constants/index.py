from enum import IntEnum

class ProjectStatus(IntEnum):
    UN_COMPLETED = 0
    COMPLETED = 1
    HAS_ERROR = 2


class TaskStatus(IntEnum):
    PENDING = 0
    SCHEDULED = 1
    RUNNING = 2
    COMPLETED = 3
    ERROR = 4


class ScheduleStatus(IntEnum):
    PAUSE = 0
    ACTIVE = 1


class TaskMode(IntEnum):
    INCREMENT = 1
    RANGE = 2
from enum import IntEnum

class ProjectStatus(IntEnum):
    UN_COMPLETED = 0
    COMPLETED = 1


class TaskStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2


class ScheduleStatus(IntEnum):
    PAUSE = 0
    ACTIVE = 1


class TaskMode(IntEnum):
    INCREMENT = 1
    RANGE = 2
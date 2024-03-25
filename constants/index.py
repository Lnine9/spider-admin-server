from enum import IntEnum

class ProjectStatus(IntEnum):
    UN_COMPLETED = 0
    COMPLETED = 1


class TaskStatus(IntEnum):
    UN_COMPLETED = 0
    COMPLETED = 1


class ScheduleStatus(IntEnum):
    PAUSE = 0
    ACTIVE = 1
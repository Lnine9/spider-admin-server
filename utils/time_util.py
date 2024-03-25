import time
from setting import DATETIME_FORMAT


def get_datetime_str():
    return time.strftime(DATETIME_FORMAT, time.localtime())


def format_datetime(datetime):
    return datetime.strftime(DATETIME_FORMAT)


if __name__ == '__main__':
    pass

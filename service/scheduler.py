from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from setting import MYSQL
import logging
from logging.handlers import RotatingFileHandler

url = f'mysql+pymysql://{MYSQL["USER"]}:{MYSQL["PASSWORD"]}@{MYSQL["HOST"]}:{MYSQL["PORT"]}/{MYSQL["DB"]}'

job_stores = {
    'default': SQLAlchemyJobStore(url=url, tablename='apscheduler_jobs')
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 5
}

scheduler = BackgroundScheduler(jobstores=job_stores, executors=executors, job_defaults=job_defaults)

apscheduler_logger = logging.getLogger('apscheduler')
scheduler._logger = apscheduler_logger

scheduler.start()


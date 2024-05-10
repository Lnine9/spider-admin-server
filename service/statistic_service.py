from service.schedule_service import ScheduleService
from service.project_service import ProjectService
from service.task_service import TaskService
from model.schedule import Schedule
from model.project import Project
from model.task import Task
from model.subject import Subject
from constants.index import ProjectStatus, TaskStatus
import datetime
import logging


class ScheduleStatistic:
    schedule_info = None
    project_count = 0
    crawl_count = 0
    resolve_count = 0
    total_run_time_min = 0
    ave_run_time_min = 0

    def __init__(self):
        pass


class ProjectStatistic:
    project_info = None
    process = 0
    task_count = 0
    running_task_count = 0
    success_task_count = 0
    error_task_count = 0
    pending_task_count = 0

    def __init__(self):
        pass


class StatisticService:
    def __init__(self):
        pass

    @classmethod
    def schedule_statistics(cls, query: dict):
        start_time = None
        end_time = None
        if query.get('start_time') is not None or query.get('end_time') is not None:
            start_time = datetime.datetime.fromtimestamp(int(query.get('start_time')))
            end_time = datetime.datetime.fromtimestamp(int(query.get('end_time')))

        result = []
        schedules = Schedule.select()
        logging.info(f"collecting schedule statistics, total: {len(schedules)}")
        for schedule in schedules:
            try:
                schedule_statistic = ScheduleStatistic()
                schedule_statistic.schedule_info = schedule.__data__
                projects = Project.select().where((Project.schedule_id == schedule.id))
                if start_time is not None and end_time is not None:
                    projects = projects.where((Project.start_time >= start_time) & (Project.end_time <= end_time))
                project_count = 0
                crawl_count = 0
                resolve_count = 0
                total_run_time_min = 0
                ave_run_time_min = 0

                for project in projects:
                    try:
                        if project.status == ProjectStatus.COMPLETED:
                            project_count += 1
                            crawl_count += project.total_crawl
                            resolve_count += project.total_resolve
                            total_run_time_min += (project.end_time - project.start_time).total_seconds() / 60
                    except Exception as e:
                        logging.error(f"project: {project.id} error: {e}")

                if project_count > 0:
                    ave_run_time_min = total_run_time_min // project_count

                schedule_statistic.project_count = project_count
                schedule_statistic.crawl_count = crawl_count
                schedule_statistic.resolve_count = resolve_count
                schedule_statistic.total_run_time_min = total_run_time_min
                schedule_statistic.ave_run_time_min = ave_run_time_min
                result.append(schedule_statistic.__dict__)
            except Exception as e:
                logging.error(f"schedule: {schedule.id} error: {e}")
        return result

    @classmethod
    def running_projects(cls):
        result = []
        logging.info(f"collecting running project statistics")
        projects = (Project
                    .select(Project, Subject.name.alias('subject_name'), Schedule.name.alias('schedule_name'))
                    .left_outer_join(Subject, on=(Project.subject_id == Subject.id))
                    .left_outer_join(Schedule, on=(Project.schedule_id == Schedule.id))
                    .where(Project.status == ProjectStatus.UN_COMPLETED))

        for project in projects:
            try:
                project_statistic = ProjectStatistic()
                project_statistic.project_info = project.__data__
                tasks = Task.select().where(Task.project_id == project.id)
                project_statistic.task_count = tasks.count()
                project_statistic.running_task_count = tasks.where(Task.status == TaskStatus.RUNNING).count()
                project_statistic.success_task_count = tasks.where(Task.status == TaskStatus.COMPLETED).count()
                project_statistic.error_task_count = tasks.where(Task.status == TaskStatus.ERROR).count()
                project_statistic.pending_task_count = tasks.where(Task.status == TaskStatus.PENDING).count()
                if project_statistic.task_count > 0:
                    project_statistic.process = project_statistic.success_task_count * 100 // project_statistic.task_count
                result.append(project_statistic.__dict__)
            except Exception as e:
                logging.error(f"project: {project.id} error: {e}")

        return result

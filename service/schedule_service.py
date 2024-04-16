from model.schedule import Schedule
from model.subject import Subject
from utils.id import generate_uuid
from service.project_service import ProjectService
from service.scheduler import scheduler
import datetime
from constants.index import ProjectStatus, TaskStatus, ScheduleStatus
from utils.index import resolve_cron
from utils.logger import logger


def job(schedule_id):
    schedule = Schedule.get_by_id(schedule_id)
    if schedule is None:
        logger.error(f"schedule_id: {schedule_id} not found")
        return

    now = datetime.datetime.now()
    print(now)
    if schedule.last_run_time is None:
        last_run_time = now - datetime.timedelta(minutes=schedule.slice_size)
    else:
        last_run_time = schedule.last_run_time

    project = {
        'name': f"{schedule.name}-{str(int(now.timestamp()))}",
        'schedule_id': schedule.id,
        'slice_size': schedule.slice_size,
        'spider_id': schedule.spider_id,
        'subject_id': schedule.subject_id,
        'range_start_time': last_run_time,
        'range_end_time': now,
        'status': ProjectStatus.UN_COMPLETED
    }
    schedule.last_run_time = now
    schedule.save()
    ProjectService.add_project(project)


class ScheduleService:
    def __init__(self):
        pass

    @classmethod
    def list_schedule(cls, params):
        query = (
            Schedule
            .select(Schedule, Subject.name.alias('subject_name'))
            .left_outer_join(Subject, on=(Schedule.subject_id == Subject.id))
            .order_by(Schedule.create_time.desc())
            .paginate(int(params.get('page_num')), int(params.get('page_size')))
        )

        result = {
            'list': query.dicts(),
            'total': query.count()
        }

        return result

    @classmethod
    def get_schedule_by_id(cls, id):
        find = (Schedule.select(Schedule, Subject.name.alias('subject_name'), Subject.id.alias('subject_id'))
                .left_outer_join(Subject).where(Schedule.id == id).dicts().get())
        return find

    @classmethod
    def add_schedule(cls, schedule):
        schedule['id'] = generate_uuid()
        schedule['status'] = ScheduleStatus.ACTIVE
        second, minute, hour, day, month, day_of_week = resolve_cron(schedule.get('cron'))
        scheduler.add_job(
            func=job,
            trigger='cron',
            id=schedule.get('id'),
            second=second, minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week,
            replace_existing=True,
            kwargs={'schedule_id': schedule.get('id')}
        )

        Schedule.create(**schedule)

    @classmethod
    def update_schedule(cls, id, new_schedule):
        local = Schedule.get(Schedule.id == id)
        local.name = new_schedule.get('name')
        local.description = new_schedule.get('description')
        local.cron = new_schedule.get('cron')
        local.slice_size = new_schedule.get('slice_size')
        local.status = ScheduleStatus.ACTIVE

        second, minute, hour, day, month, day_of_week = resolve_cron(local.cron)
        scheduler.reschedule_job(
            job_id=id,
            trigger='cron',
            second=second, minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week,
        )
        local.save()

    @classmethod
    def delete_schedule(cls, id):
        local = Schedule.get(Schedule.id == id)
        local.delete_instance()

        scheduler.remove_job(id)

    @classmethod
    def change_status(cls, id, status):
        local = Schedule.get(Schedule.id == id)

        if status == ScheduleStatus.PAUSE:
            scheduler.pause_job(id)
        elif status == ScheduleStatus.ACTIVE:
            scheduler.resume_job(id)

        local.status = status
        local.save()


if __name__ == '__main__':
    q = Schedule.select(Schedule, Subject.name.alias('subject_name')).left_outer_join(Subject,
                                                                           on=(Schedule.subject_id == Subject.id))
    print(list(q.dicts()))

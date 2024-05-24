from service.statistic_service import StatisticService
from flask import request
from utils.flask_ext.flask_app import BlueprintAppApi

statistic_api = BlueprintAppApi(name="statistic", import_name=__name__)


@statistic_api.get('/schedule_statistic')
def schedule_statistic():
    params = request.args.to_dict()
    return StatisticService.schedule_statistics(params)


@statistic_api.get('/running_projects')
def running_projects():
    return StatisticService.running_projects()


@statistic_api.get('/last_24h_task_count')
def last_24h_task_count():
    return StatisticService.last_24h_task_count()
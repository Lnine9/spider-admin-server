def resolve_cron(cron):
    crons = cron.split(' ')
    crons = filter(lambda x: x, crons)
    second, minute, hour, day, month, day_of_week = crons
    return second, minute, hour, day, month, day_of_week


def clean_params(params):
    if not params:
        return {}
    return {k: v for k, v in params.items() if v is not None and v != ''}

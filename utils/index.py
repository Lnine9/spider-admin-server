def resolve_cron(cron):
    crons = cron.split(' ')
    crons = filter(lambda x: x, crons)
    second, minute, hour, day, month, day_of_week = crons
    return second, minute, hour, day, month, day_of_week

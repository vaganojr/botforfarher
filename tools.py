import datetime
import pytz


TIME_ZONE = 'Europe/Moscow'


def get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone(TIME_ZONE)
    now = datetime.datetime.now(tz)
    return now

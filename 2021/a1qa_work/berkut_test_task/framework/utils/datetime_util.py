# coding=utf-8
from datetime import datetime, timezone, timedelta
from random import randrange


class DatetimeUtil(object):

    @staticmethod
    def random_date(start=datetime(1900, 1, 1), end=datetime.now()):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    @staticmethod
    def get_str_datetime(exp_format):
        return datetime.now().strftime(exp_format)

    @staticmethod
    def get_current_time(offset_from_utc=0, date_time_format="%H:%M"):
        utc_dt = datetime.now(timezone.utc)
        dt = utc_dt.replace(hour=utc_dt.time().hour + offset_from_utc)
        return dt.strftime(date_time_format)

    @staticmethod
    def datetimes_are_equal_sec_precision(datetime1: datetime, datetime2: datetime, sec_precision=1) -> bool:
        return (datetime1.year == datetime2.year
                and datetime1.month == datetime2.month
                and datetime1.day == datetime2.day
                and datetime1.hour == datetime2.hour
                and datetime1.minute == datetime2.minute
                and abs(datetime1.second - datetime2.second) <= sec_precision)

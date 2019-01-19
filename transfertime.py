# coding:utf-8

import datetime
import pytz
import re

__author__ = 'martin'


class TransferTime(object):
    """时间转换类"""
    def __init__(self, date):
        if isinstance(date, datetime.datetime):
            self.__date = date.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            date = str(date) if isinstance(date, int) else date
            self.__date = date.replace('T', ' ').replace('Z', '')
        # 初始格式
        self.__format = self.__get_format(self.__date)
        self.__new_format = self.__format
        if self.__format is None:
            raise TypeError('%s not date format' % date)

        self.__add = 0
        self.__reduce = 0
        self.__add_minute = 0
        self.__reduce_minute = 0
        self.__local_tz = pytz.timezone(pytz.country_timezones('cn')[0])
        self.__new_tz = self.__local_tz

    def set_zone(self, zone_name):
        """设置时区"""
        # 时区转换
        try:
            tz = pytz.timezone(pytz.country_timezones(zone_name)[0])
        except:
            tz = pytz.timezone(pytz.country_timezones('hk')[0])
            #raise TypeError('Zone: %s not found' % zone_name)
        self.__new_tz = tz
        return self

    def set_market_zone(self, market_name):
        """获取区域"""
        if market_name.upper() in ['SZ', 'SH']:
            zone = 'cn'
        elif market_name.upper() == 'US':
            zone = 'us'
        else:
            zone = 'hk'
        self.set_zone(zone)
        return self

    def __datetime(self, _format=None, _conv='datetime'):
        _format = self.__format if not _format else self.__new_format
        # str -> datetime
        date = datetime.datetime.strptime(self.__date, self.__format)
        date = date + datetime.timedelta(days=self.__add)
        date = date - datetime.timedelta(days=self.__reduce)
        date = date + datetime.timedelta(minutes=self.__add_minute)
        date = date - datetime.timedelta(minutes=self.__reduce_minute)

        date = self.__local_tz.localize(date).astimezone(self.__new_tz)
        # datetime -> str
        if _conv == 'zone':
            return date
        elif _conv != 'datetime':
            return date.strftime(_format)
        else:
            date = date.strftime(_format)
            return datetime.datetime.strptime(date, self.__get_format(date))

    def __sub__(self, value):
        """两个时间相隔多少天"""
        return self.datetime - value.datetime

    def add_day(self, day: int):
        """增加天数"""
        self.__add += day
        return self

    def reduce_day(self, day: int):
        """减小天数"""
        self.__reduce += day
        return self

    def add_minute(self, minute: int):
        self.__add_minute += minute
        return self

    def reduce_minute(self, minute: int):
        self.__reduce_minute += minute
        return self

    @property
    def reset_date(self):
        self.__add = 0
        self.__reduce = 0
        self.__add_minute = 0
        self.__reduce_minute = 0
        return self

    @property
    def year(self):
        return self.__datetime().strftime('%Y')

    @property
    def month(self):
        return self.__datetime().strftime('%m')

    @property
    def day(self):
        return self.__datetime().strftime('%d')

    @property
    def hour(self):
        return self.__datetime().strftime('%H')

    @property
    def minute(self):
        return self.__datetime().strftime('%M')

    @property
    def second(self):
        return int(self.__datetime().strftime('%S'))

    @property
    def microsecond(self):
        return int(self.__datetime().strftime('%f'))

    @property
    def timestamp(self):
        epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        date = self.__datetime(_conv='zone').astimezone(pytz.utc)
        return datetime.timedelta.total_seconds(date - epoch)

    @property
    def reset_zone(self):
        self.__new_tz = self.__local_tz
        return self

    def set_format(self, format):
        """设置格式"""
        # test
        try:
            datetime.datetime.strptime(self.__date, self.__format).strftime(format)
        except Exception:
            raise TypeError('formt error: %s' % format)
        self.__new_format = format
        return self

    @property
    def reset_format(self):
        self.__new_format = self.__format
        return self

    @property
    def datetime(self):
        """返回datetime"""
        # str-> datetime
        _format = self.__new_format if self.__new_format != self.__format else None
        date = self.__datetime(_format=_format)
        return date

    @property
    def c_datetime(self):
        date = self.datetime
        date = date.replace(tzinfo=None)
        return date

    @property
    def str(self):
        """返回str"""
        # str -> datetime
        date = self.__datetime(_conv='str', _format=self.__new_format)
        return date

    def __str__(self):
        return self.str

    @staticmethod
    def __get_format(date):
        date_format = None
        if date.find('-') >0 and len(date.split('-')) == 3:
            # '%Y-%m-%d %H:%M:%S'
            if date.find(':') >0:
                if len(date.split(':')) == 3:
                    if len(date.split(':')[-1].split('.')) == 2:
                        date_format = '%Y-%m-%d %H:%M:%S.%f'
                    else:
                        date_format = '%Y-%m-%d %H:%M:%S'
                elif len(date.split(':')) == 2:
                    date_format = '%Y-%m-%d %H:%M'
            else:
                date_format = '%Y-%m-%d'
        else:
            r = re.compile('\d{1,}$')
            if r.match(date):
                if len(date) == 8:
                    date_format = '%Y%m%d'
                elif len(date) == 12:
                    date_format = '%Y%m%d%H%M'
                elif len(date) == 14:
                    date_format = '%Y%m%d%H%M%S'
        return date_format




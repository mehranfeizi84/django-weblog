from . import jalali
from django.utils import timezone


def jalali_converter(time):
    # jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
    #           'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time = timezone.localtime(time)

    date_string = f"{time.day} ,{time.month} ,{time.year}"
    time_string = f"{time.hour}:{time.minute}"

    # time_jalali = jalali.Gregorian(time_string).persian_string()
    # time_tuple = jalali.Gregorian(time_string).persian_tuple()

    # time_list = list(time_tuple)

    # for index, month in enumerate(jmonth):
    #     if time_list[1] == index:
    #         time_list[1] == month
    #         break

    # output = f"{time_list[2]} {time_list[1]} {time_list[0]} ساعت : {time.hour}:{time.minute}"

    return f"{time_string} | {date_string}"

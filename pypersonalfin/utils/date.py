from datetime import datetime, date
from urllib.parse import parse_qs

from .locale import is_brazil


def convert_to_date(date_str, locale):
    today = date.today()
    if is_brazil(locale):
        if date_str.lower().strip() == 'hoje':
            return today
        elif date_str.lower().strip() == 'mes':
            return date(today.year, today.month, 1)

        try:
            final_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            return final_date
        except ValueError:
            pass

    if date_str.lower().strip() == 'today':
        return today
    elif date_str.lower().strip() == 'month':
        return date(today.year, today.month, 1)

    # Fallback to US date
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def date_to_str(date, locale):
    if is_brazil(locale):
        return date.strftime('%d/%m/%Y')

    # Fallback to US date
    return date.strftime('%Y-%m-%d')


def _deep_update_dicts(original, update):
    if not original:
        return update

    for key, value in original.items():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            _deep_update_dicts(value, update[key])

    return update


def get_date_range(begin, end, locale):
    dates_per_parser = {}

    begin_dates = parse_qs(begin)

    begin_dates = {
        key: {"begin": convert_to_date(value[0], locale)} for key, value in begin_dates.items()
    } if begin_dates else None

    dates_per_parser = _deep_update_dicts(begin_dates, dates_per_parser)

    end_dates = parse_qs(end)
    end_dates = {
        key: {"end": convert_to_date(value[0], locale)} for key, value in end_dates.items()
    } if end_dates else None
    dates_per_parser = _deep_update_dicts(end_dates, dates_per_parser)

    date_begin = None
    date_end = None

    if dates_per_parser:
        for dates in dates_per_parser.values():
            current_date_begin = dates['begin']
            current_date_end = dates['end']
            if not date_begin or current_date_begin < date_begin:
                date_begin = current_date_begin
            if not date_end or current_date_end > date_end:
                date_end = current_date_end
    else:
        date_begin = convert_to_date(begin, locale)
        date_end = convert_to_date(end, locale)

    return date_begin, date_end, dates_per_parser

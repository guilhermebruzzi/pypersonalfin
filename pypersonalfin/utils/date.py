from datetime import datetime

from .locale import is_brazil


def convert_to_date(date_str, locale):
    if is_brazil(locale):
        try:
            date = datetime.strptime(date_str, '%d/%m/%Y').date()
            return date
        except ValueError:
            pass

    # Fallback to US date
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def date_to_str(date, locale):
    if is_brazil(locale):
        return date.strftime('%d/%m/%Y')

    # Fallback to US date
    return date.strftime('%Y-%m-%d')

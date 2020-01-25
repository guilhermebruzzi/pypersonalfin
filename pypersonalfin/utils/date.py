from datetime import datetime, date

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


def get_date_range(begin, end, locale):
    date_begin = convert_to_date(begin, locale)
    date_end = convert_to_date(end, locale)

    return date_begin, date_end

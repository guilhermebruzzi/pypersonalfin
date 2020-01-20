from datetime import datetime


def convert_to_date(date_str, locale):
    if locale.lower() == 'pt-br' or locale.lower() == 'pt_br':
        date = datetime.strptime(date_str, '%d/%m/%Y').date()
        return date

    # Fallback to US date
    return datetime.strptime(date_str, '%Y-%m-%d').date()

from .locale import is_brazil


def amount_to_str(amount, locale=None, include_currency=True):
    float_amount = amount / 100.0
    # Fallback to US amount
    float_amount_str = "{:.2f}".format(float_amount)

    if is_brazil(locale):
        float_amount_str = float_amount_str.replace('.', ',')
        if include_currency:
            return 'R${}'.format(float_amount_str)
        return float_amount_str

    if include_currency:
        return '${}'.format(float_amount_str)

    return float_amount_str

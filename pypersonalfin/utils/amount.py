def amount_to_str(amount, locale):
    float_amount = amount / 100.0
    float_amount_str = "{:.2f}".format(float_amount)

    if locale.lower() == 'pt-br' or locale.lower() == 'pt_br':
        return float_amount_str.replace('.', ',')

    # Fallback to US amount
    return float_amount_str

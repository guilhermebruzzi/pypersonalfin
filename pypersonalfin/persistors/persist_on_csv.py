def _get_name_from_categories(categories):
    lower_bound_date = categories[0].lower_bound_date
    upper_bound_date = categories[0].upper_bound_date

    for category in categories:
        if category.upper_bound_date > upper_bound_date:
            upper_bound_date = category.upper_bound_date

        if category.lower_bound_date < lower_bound_date:
            lower_bound_date = category.lower_bound_date

    return "{}-{}".format(lower_bound_date, upper_bound_date)


def _persist(categories, name):
    print("Persist on {} the following categories:".format(name))
    print("{}".format([category.to_csv() for category in categories]))
    return


def persist_on_csv(categories, name=None):
    if not categories or len(categories) == 0:
        return

    if not name:
        name = _get_name_from_categories(categories)

    _persist(categories, name)

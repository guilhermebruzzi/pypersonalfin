def _persist(categories_csv, file_name):
    print("\nPersist on {}:\n\n".format(file_name))
    print(categories_csv)
    return


def persist_on_csv(categories_csv, file_name):
    if not categories_csv:
        return

    if ".csv" not in file_name:
        file_name = "{}.csv".format(file_name)

    _persist(categories_csv, file_name)

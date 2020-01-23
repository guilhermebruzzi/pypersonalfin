from utils.file import save_file_on_output_folder


def _persist(categories_csv, file_name):
    save_file_on_output_folder(file_name, categories_csv)


def persist_on_csv(categories_csv, file_name):
    if not categories_csv:
        return

    if ".csv" not in file_name:
        file_name = "{}.csv".format(file_name)

    _persist(categories_csv, file_name)

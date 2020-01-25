#!/usr/bin/env python3
import os
import sys
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials

from run import main as run_script
from utils.file import get_src_folder_abs_path, get_output_folder_abs_path

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def main(args):
    if len(args) < 2:
        print('Please pass at least 2 arguments: the spreadsheet name and either if you will run the script or the file name of the previous run')
        exit(1)

    name = args[0]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        get_src_folder_abs_path('service_credentials.json'), scope
    )

    gc = gspread.authorize(credentials)

    print("Opening spreadsheet: {}".format(name))
    sh = gc.open(name)

    file_name = args[1].lower()
    run = False
    if len(args) > 1:
        run = file_name == 'true'

    if run:
        locale = 'en_us'
        if len(args) > 2:
            locale = args[2]

        begin = None
        if len(args) > 3:
            begin = args[3]

        end = None
        if len(args) > 4:
            end = args[4]

        print('Running pypersonalfin script...')
        file_name = run_script(locale, begin, end)

    with open(get_output_folder_abs_path(file_name)) as reader:
        file_name = os.path.splitext(file_name)[0]

        print("Adding worksheet {}".format(file_name))

        sh.add_worksheet(title=file_name, rows=100, cols=1000)

        values = list(csv.reader(reader, delimiter=';'))

        sh.values_update(
            file_name,
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': values}
        )


if __name__ == "__main__":
    main(sys.argv[1:])

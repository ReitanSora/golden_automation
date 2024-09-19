from config import download
import pandas as pd
import os
from utils.services.download_file import get_file, get_files, get_files_by_pattern
from utils.services.update_document import update

FOLDER_NAME = download['folder_name']
FILE_NAME = download['file_name']
FILE_NAME_PATTERN = download['file_name_pattern']

def read_excel():
    df = pd.read_excel('./storage/Peru.xlsx')
    print(df.head())
    update()

if __name__ == '__main__':
    if FILE_NAME != 'None':
        get_file(FILE_NAME, FOLDER_NAME)
    elif FILE_NAME_PATTERN != 'None':
        get_files_by_pattern(FILE_NAME_PATTERN, FOLDER_NAME)
    else:
        get_files(FOLDER_NAME)

    read_excel()
    #os.remove('./storage/Peru.xlsx')



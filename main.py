from config import download
import pandas as pd
import os
from utils.services.download_file import get_file, get_files, get_files_by_pattern

# 1 args = SharePoint folder name. May include subfolders YouTube/2022
FOLDER_NAME = download['folder_name']
# 3 args = SharePoint file name. This is used when only one file is being downloaded
# If all files will be downloaded, then set this value as "None"
FILE_NAME = download['file_name']
# 4 args = SharePoint file name pattern
# If no pattern match files are required to be downloaded, then set this value as "None"
FILE_NAME_PATTERN = download['file_name_pattern']


def read_excel():
    df = pd.read_excel('./storage/Peru.xlsx')
    print(df.head())

if __name__ == '__main__':
    if FILE_NAME != 'None':
        get_file(FILE_NAME, FOLDER_NAME)
    elif FILE_NAME_PATTERN != 'None':
        get_files_by_pattern(FILE_NAME_PATTERN, FOLDER_NAME)
    else:
        get_files(FOLDER_NAME)

    read_excel()
    os.remove('./storage/Peru.xlsx')



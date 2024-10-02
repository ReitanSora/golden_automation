from config import download
from src.services.download_file import get_file, get_files, get_files_by_pattern
from src import init_app


def initialize_app():
    app = init_app()
    return app


if __name__ == '__main__':
    if download['file_name'] != 'None':
        get_file(download['file_name'], download['folder_name'])
    elif download['file_name_pattern'] != 'None':
        get_files_by_pattern(
            download['file_name_pattern'], download['folder_name'])
    else:
        get_files(download['folder_name'])

    app = initialize_app()
    app.run()

from flask import Flask
from config import download
from src.services.download_file import get_file, get_files, get_files_by_pattern
from src.services.update_document import update
from src.routes.coord_routes import coord_bp

FOLDER_NAME = download['folder_name']
FILE_NAME = download['file_name']
FILE_NAME_PATTERN = download['file_name_pattern']

app = Flask(__name__)

# Registrar el Blueprint
app.register_blueprint(coord_bp)


@app.route('/')
def root():
    return "root"


def read_update_excel():
    update()


if __name__ == '__main__':
    if FILE_NAME != 'None':
        get_file(FILE_NAME, FOLDER_NAME)
    elif FILE_NAME_PATTERN != 'None':
        get_files_by_pattern(FILE_NAME_PATTERN, FOLDER_NAME)
    else:
        get_files(FOLDER_NAME)

    read_update_excel()
    app.run(debug=False)

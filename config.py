from decouple import config
import os

sharepoint = {
    'user_email': config('SHAREPOINT_EMAIL'),
    'user_password': config('SHAREPOINT_PASSWORD'),
    'sharepoint_site': config('SHAREPOINT_URL_SITE'),
    'sharepoint_site_name': config('SHAREPOINT_SITE_NAME'),
    'sharepoint_doc_library': config('SHAREPOINT_DOC_LIBRAY')
}

download = {
    'folder_name': config('FOLDER_NAME'),
    'folder_download_target': os.path.abspath('./storage'),
    'file_name': config('FILE_NAME'),
    'file_name_pattern': config('FILE_NAME_PATTERN')
}

mongo = {
    'mongodb_url': config('MONGODB_URL'),
    'mongodb_db_name': config('MONGODB_DB_NAME'),
}
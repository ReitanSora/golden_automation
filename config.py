from decouple import config
import os

sharepoint = {
    'user_email': config('SHAREPOINT_EMAIL'),
    'user_password': config('SHAREPOINT_PASSWORD'),
    'sharepoint_site': config('SHAREPOINT_URL_SITE'),
    'sharepoint_site_name': config('SHAREPOINT_SITE_NAME'),
    'sharepoint_doc_library': config('SHAREPOINT_DOC_LIBRAY'),
    'sharepoint_root_dir_upload': os.path.abspath('./storage'),
    'sharepoint_folder_name_upload': config('SHAREPOINT_FOLDER_NAME_UPLOAD'),
    'file_name_pattern_upload': config('FILE_NAME_PATTERN_UPLOAD')
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
    'mongodb_db_name_coordinates': config('MONGODB_DB_NAME_COORDINATES'),
    'mongodb_fb_collection': config('MONGODB_FB_COLLECTION'),
    'mongodb_ig_collection': config('MONGODB_IG_COLLECTION'),
    'mongodb_tw_collection': config('MONGODB_TW_COLLECTION'),
    'mongodb_yt_collection': config('MONGODB_YT_COLLECTION'),
    'mongodb_tk_collection': config('MONGODB_TK_COLLECTION'),
    'mongodb_fb_field_name': config('MONGODB_FB_FIELD_NAME'),
    'mongodb_ig_field_name': config('MONGODB_IG_FIELD_NAME'),
    'mongodb_tw_field_name': config('MONGODB_TW_FIELD_NAME'),
    'mongodb_yt_field_name': config('MONGODB_YT_FIELD_NAME'),
    'mongodb_tk_field_name': config('MONGODB_TK_FIELD_NAME'),
}

excel = {
    'file_name': config('FILE_NAME'),
    'excel_subzone_1': config('EXCEL_SUBZONE_1'),
    'excel_subzone_2': config('EXCEL_SUBZONE_2'),
    'excel_subzone_3': config('EXCEL_SUBZONE_3'),
    'excel_subzone_4': config('EXCEL_SUBZONE_4'),
    'excel_subzone_5': config('EXCEL_SUBZONE_5'),
}

gpt = {
    'gpt_api_key': config('GPT_API_KEY'),
}

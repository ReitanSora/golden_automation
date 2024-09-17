## Environment Variables

The environment variables should be of the following form in the .env file:

- SHAREPOINT_EMAIL="Here you variable"
- SHAREPOINT_PASSWORD="Here you variable"
- SHAREPOINT_URL_SITE="Here you variable"
- SHAREPOINT_SITE_NAME="Here you variable"
- SHAREPOINT_DOC_LIBRAY="Here you variable"
- FOLDER_NAME="Here you variable"
- FILE_NAME="Here you variable"
- FILE_NAME_PATTERN="Here you variable"

### FILE_NAME Variable

In this variable you must specify the file you want to download, otherwise set None so that all files from the specified path are downloaded.

### FILE_NAME_PATTERN Variable

In this variable you must specify a pattern in the name of the files you want to download, if there is no pattern you must set it to None.
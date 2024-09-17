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

### SHAREPOINT_EMAIL & SHAREPOINT_PASSWORD Variables

These variables are to authenticate you in sharepoint and access the files you want to download.

### SHAREPOINT_URL_SITE Variable

To set this variable, you must go to sharepoint and select the site you prefer.

You have to copy the url from the site you select, you should have a url like the following.
Example: "https://domain.sharepoint.com/sites/test2"

### SHAREPOINT_SITE_NAME Variable

The value for this variable is the name of the site or group from the url we previously obtained.
Example: test2

### SHAREPOINT_DOC_LIBRARY Variable

The general path of our files should go in this variable. To do this you must access the documents part of the menu on the left once you are inside the chosen site, then in the url you will find something like this:

Example: "https://domain.sharepoint.com/sites/test2/Documentos%20compartidos/----/-----"

Now, in our variable you must place: "Documentos compatidos/"

### FOLDER_NAME Variable

This variable must include the name of the folder that contains the files.

### FILE_NAME Variable

In this variable you must specify the file you want to download, otherwise set None so that all files from the specified path are downloaded.

### FILE_NAME_PATTERN Variable

In this variable you must specify a pattern in the name of the files you want to download, if there is no pattern you must set it to None.
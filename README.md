# 📝 Project README

## ⚙️ Environment Variables

Define the following environment variables in your `.env` file to configure the project:

```plaintext
# SharePoint Variables
SHAREPOINT_EMAIL="your_email"                  # Required, with quotes
SHAREPOINT_PASSWORD="your_password"            # Required, with quotes
SHAREPOINT_URL_SITE="https://your_site_url"    # Required, with quotes
SHAREPOINT_SITE_NAME="your_site_name"          # Required, with quotes
SHAREPOINT_DOC_LIBRARY="your_document_library" # Required, with quotes

# File Handling
FOLDER_NAME="your_folder_name"                 # Required, with quotes
FILE_NAME="your_file_name_or_None"             # Set a file name or None, quotes required
FILE_NAME_PATTERN="your_pattern_or_None"       # Set a pattern or None, quotes required

# MongoDB Variables
MONGODB_URL="mongodb://localhost:27017/"       # Required, with quotes
MONGODB_DB_NAME="your_db_name"                 # Required, with quotes
MONGODB_DB_NAME_COORDINATES="your_db_name"     # Required, with quotes

# SharePoint Uploads
SHAREPOINT_FOLDER_NAME_UPLOAD="your_upload_folder"   # Required, with quotes
FILE_NAME_PATTERN_UPLOAD="your_pattern_or_None"      # Set a pattern or None, quotes required

# GPT API Key
GPT_API_KEY="your_gpt_api_key"                 # Required, with quotes

# MongoDB Collections & Fields
MONGODB_FB_COLLECTION="your_fb_collection"     # Required, with quotes
MONGODB_IG_COLLECTION="your_ig_collection"     # Required, with quotes
MONGODB_TW_COLLECTION="your_tw_collection"     # Required, with quotes
MONGODB_YT_COLLECTION="your_yt_collection"     # Required, with quotes
MONGODB_TK_COLLECTION="your_tk_collection"     # Required, with quotes

MONGODB_FB_FIELD_NAME="username"               # Required, with quotes
MONGODB_IG_FIELD_NAME="username"               # Required, with quotes
MONGODB_TW_FIELD_NAME="screenName"             # Required, with quotes
MONGODB_YT_FIELD_NAME="_id"                    # Required, with quotes
MONGODB_TK_FIELD_NAME="username"               # Required, with quotes

# Excel Subzones
EXCEL_SUBZONE_1="Sublevel 1"                   # Required, with quotes
EXCEL_SUBZONE_2="Sublevel 2"                   # Required, with quotes
EXCEL_SUBZONE_3="Sublevel 3"                   # Required, with quotes
EXCEL_SUBZONE_4="Sublevel 4"                   # Required, with quotes
EXCEL_SUBZONE_5="Sublevel 5"                   # Required, with quotes
```

### 🔍 Variable Details

1. **SHAREPOINT_EMAIL** & **SHAREPOINT_PASSWORD**
   - Used for authenticating with SharePoint. These values must be wrapped in double quotes (`""`).

2. **SHAREPOINT_URL_SITE**
   - URL of the SharePoint site you want to access. Example: `"https://yourcompany.sharepoint.com/sites/yoursite"`.

3. **SHAREPOINT_DOC_LIBRARY**
   - Path to the document library inside SharePoint. Example: `"Documents Shared/"`.

4. **FILE_NAME** & **FILE_NAME_PATTERN**
   - Use `"None"` if you want to download all files or if no pattern is required.

5. **MONGODB_URL** & **Database Names**
   - MongoDB connection string and database names must be wrapped in quotes. Example: `"mongodb://localhost:27017/"`.

6. **GPT_API_KEY**
   - Your GPT API key for enabling AI functionalities in your app. Must be wrapped in quotes.

7. **Collection and Field Names**
   - Each social media platform (Facebook, Instagram, etc.) uses a unique collection and field name. Ensure these are clearly specified and enclosed in quotes.

8. **Excel Subzones**
   - These fields represent subzones in your Excel data. Adjust as needed based on your data structure.

### 📋 Example Configuration

Here is an example of a properly filled `.env` file for your reference:

```plaintext
SHAREPOINT_EMAIL="user@example.com"
SHAREPOINT_PASSWORD="SuperSecretPassword"
SHAREPOINT_URL_SITE="https://yourcompany.sharepoint.com/sites/projectsite"
SHAREPOINT_SITE_NAME="projectsite"
SHAREPOINT_DOC_LIBRARY="Documents Shared/"
FOLDER_NAME="project/documents"
FILE_NAME="data.xlsx"
FILE_NAME_PATTERN=None

MONGODB_URL="mongodb://localhost:27017/"
MONGODB_DB_NAME="mydatabase"
MONGODB_DB_NAME_COORDINATES="coordinates"

SHAREPOINT_FOLDER_NAME_UPLOAD="project/uploads"
FILE_NAME_PATTERN_UPLOAD="Updated"

GPT_API_KEY="your_gpt_api_key"

MONGODB_FB_COLLECTION="fb_collection"
MONGODB_IG_COLLECTION="ig_collection"
MONGODB_TW_COLLECTION="tw_collection"
MONGODB_YT_COLLECTION="yt_collection"
MONGODB_TK_COLLECTION="tk_collection"

MONGODB_FB_FIELD_NAME="username"
MONGODB_IG_FIELD_NAME="username"
MONGODB_TW_FIELD_NAME="screenName"
MONGODB_YT_FIELD_NAME="_id"
MONGODB_TK_FIELD_NAME="username"

EXCEL_SUBZONE_1="Sublevel 1"
EXCEL_SUBZONE_2="Sublevel 2"
EXCEL_SUBZONE_3="Sublevel 3"
EXCEL_SUBZONE_4="Sublevel 4"
EXCEL_SUBZONE_5="Sublevel 5"
```

### 🚀 How to Use

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    ```

2. **Set Up the Environment Variables**:
    - Create a `.env` file in the root directory.
    - Copy the environment variables listed above into your `.env` file and replace `"your_variable"` with your actual values.

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```bash
    python app.py
    ```

### 📂 File Structure

Ensure the project files follow a well-organized structure:

```
/project_root
│
├── src/
│   ├── database/        # Handles database connections and queries
│   ├── routes/          # Contains API endpoints and routing logic
│   ├── models/          # Database models
│   ├── services/        # Business logic (CRUD operations, etc.)
│   ├── utils/           # Utilities (logging, security, etc.)
│   └── tests/           # Unit tests
│
├── .env                 # Environment variables (never commit this file)
├── .gitignore           # Specifies files to ignore in version control
├── README.md            # Project instructions (this file)
├── requirements.txt     # Python dependencies
└── app.py               # Main entry point for running the application
```

### 🔒 Security

- **.env File**: Ensure your `.env` file is included in `.gitignore` to prevent exposing sensitive data (credentials, API keys) in version control.
  
- **Best Practices**: Regularly rotate credentials and use environment variables for managing secrets and sensitive configuration.
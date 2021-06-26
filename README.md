## Pre-Signed-URL-Generator
The Pre-Signed-URL-Generator gives Pre-signed-urls to users who don't have permission to directly run AWS operations for the files present in the S3 bucket of your account. A pre-signed URL is signed with your
 credentials and can be used by any user.


## Getting Started
Follow the instruction to setup the Flask application on your local system.

## Create Virtual Environment
```
virtialenv venv
source venv/bin/activate
```

## Install Requirements
```
pip install -r requirements.txt
```

## Update 'connection.properties' file with EXPIRY (of signed url), REGION_NAME, BUCKET_NAME, ACCESS_KEY, SECRET_KEY

## Update 'files.json' file with the keys present in the S3 bucket

## To run the program in local server use the following command
```
python api.py
Then go to http://127.0.0.1:5000/ in your browser
```

## Available endpoints

- `GET` **/documents** - It returns all signed-url for all the files mentioned in 'files.json' file
- `POST` **/documents/resend** - Its a post call to get the singed-urls again who got expired.
    Post call body includes the list of the failed-signed-urls.
    {
        "files": ["Failed-signed-url"]
    }



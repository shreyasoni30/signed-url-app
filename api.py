import json
from urllib.parse import urlparse
from flask import Flask, request, jsonify

from utils import AWSService

app = Flask(__name__)
app.config["DEBUG"] = True


# Reading files from files.json
def read_json():
    object_list = []
    with open("files.json", "r") as json_file:
        data = json.load(json_file)
        for obj in data['data']:
            object_list.append(obj['key'])
    return object_list


@app.route('/', methods=['GET'])
def home():
    return {"Available Endpoints": ["http://127.0.0.1:5000/documents", "http://127.0.0.1:5000/documents/resend"]}


@app.route('/documents', methods=['GET'])
def documents():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', None, type=int)

    file_keys = read_json()

    total_files = len(file_keys)
    files = []
    payload = {
        "files": [],
        "next_page": None,
        "total": total_files,
    }
    aws = AWSService()
    if not page_size or page_size > total_files:
        start = 0
        end = total_files
    else:
        start = (page - 1) * page_size
        end = start + page_size
        if end >= total_files:
            payload["next_page"] = None
        else:
            payload[
                "next_page"] = f"/documents/?page={page + 1}&page_size={page_size}"

    for key in file_keys[start:end]:
        signed_url, timestamp = aws.create_presigned_url(key)
        files.append({
            "file": key,
            "timestamp": timestamp,
            "signed_url": signed_url,
            "expiry_time": aws.expiry
        })
    payload["files"] = files
    return jsonify(payload)


@app.route('/documents/resend', methods=['POST'])
def resend():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', None, type=int)

    aws = AWSService()
    exp_urls = request.json
    total_files = len(exp_urls["files"])
    payload = {
        "total": total_files,
        "files": [],
        "next_page": None
    }
    files = []
    if not page_size or page_size > total_files:
        start = 0
        end = total_files
    else:
        start = (page - 1) * page_size
        end = start + page_size
        if end >= total_files:
            payload["next_page"] = None
        else:
            payload["next_page"] = f"/documents/resend/?page={page + 1}&page_size={page_size}"

    for url in exp_urls["files"][start:end]:
        key = urlparse(url).path
        signed_url, timestamp = aws.create_presigned_url(key[1:])
        files.append({
            "timestamp": timestamp,
            "signed_url": signed_url,
            "expiry_time": aws.expiry
        })
    payload["files"] = files

    return jsonify(payload)


if __name__ == "__main__":
    app.run()

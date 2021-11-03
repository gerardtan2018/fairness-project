import os

os.environ['GOOGLE_SERVICE_JSON_FILE'] = r"..\creds.json"
print(os.environ['GOOGLE_SERVICE_JSON_FILE'])
GOOGLE_SERVICE_JSON_FILE = os.environ['GOOGLE_SERVICE_JSON_FILE']
BACKEND_PORT = 10000

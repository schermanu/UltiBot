# Imports the Google Cloud client library
from google.cloud import storage
import json
datajson = json.dumps(myServerData)

# Instantiates a client
client = storage.Client()

# Creates a new bucket and uploads an object
bucket = client.bucket('data-ultibot')
blob = bucket.blob('servers-param.json')
blob.upload_from_string(datajson)
data = json.loads(blob.download_as_string(client=None))
print(data['age'])
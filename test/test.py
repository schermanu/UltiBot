# Imports the Google Cloud client library
from google.cloud import storage
import json

myServerData = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
datajson = json.dumps(myServerData)
# Instantiates a client
client = storage.Client()

# Creates a new bucket and uploads an object
bucket = client.bucket('data-ultibot')
blob = bucket.blob('servers-param.json')
blob.upload_from_string(datajson)
data = json.loads(blob.download_as_string(client=None))
print(data['age'])
# Retrieve an existing bucket
# https://console.cloud.google.com/storage/browser/[bucket-id]/
# bucket = client.get_bucket('bucket-id')
# # Then do other things...
# blob = bucket.get_blob('remote/path/to/file.txt')
# print(blob.download_as_bytes())
# blob.upload_from_string('New contents!')

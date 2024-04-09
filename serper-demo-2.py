import http.client
import json
import os

conn = http.client.HTTPSConnection("google.serper.dev")
payload = json.dumps({
  "q": "apple inc"
})
headers = {
  'X-API-KEY':  os.environ['SERPER_API_KEY'],
  'Content-Type': 'application/json'
}
conn.request("POST", "/search", payload, headers)
res = conn.getresponse()
data = json.loads(res.read().decode())
print(data["organic"])
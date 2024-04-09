import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

url = "https://google.serper.dev/search"

payload = json.dumps({
  "q": "apple inc"
})
headers = {
   'X-API-KEY': os.environ['SERPER_API_KEY'],
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
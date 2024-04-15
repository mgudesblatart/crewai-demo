import json

import http.client
from crewai_tools import tool

JIRA_AUTH_KEY='Basic Y29ubm9ydmFsYW5AZ21haWwuY29tOkFUQVRUM3hGZkdGMEc4X1dkVXNTVDFFWVB5TnFkUW1zT2l6d2FVWGZIN05FZ0I3Qm5RX2tUX25jZkNQTGoyZkdaWkZjMG4wSmphUVByMXViczR4YkFFNlh3YkxudkV0ZDk0Y0JMMG9CNDkyd1lzY1ZuZ09HakQ0bElydGlzQXhzS2xPUGN4ZXlwQTdyRThJSHZCa25KMlJiOG0wYU5JNl9wUDlzbldzWTFKR0d2UWxTUm1nT3VGOD00RDcyRkY5Mw=='

issueKey = "KAN-123"
apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
headers = {
    'Authorization': JIRA_AUTH_KEY,
    'Content-Type': 'application/json'
}
url = f'/rest/api/3/issue/{issueKey}'
print(url)
apiConnection.request("GET", url, headers=headers)
res = apiConnection.getresponse()
data = json.loads(res.read().decode())
print(data)
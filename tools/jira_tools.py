import json

import http.client
from crewai_tools import tool

JIRA_AUTH_KEY='Basic Y29ubm9ydmFsYW5AZ21haWwuY29tOkFUQVRUM3hGZkdGMEc4X1dkVXNTVDFFWVB5TnFkUW1zT2l6d2FVWGZIN05FZ0I3Qm5RX2tUX25jZkNQTGoyZkdaWkZjMG4wSmphUVByMXViczR4YkFFNlh3YkxudkV0ZDk0Y0JMMG9CNDkyd1lzY1ZuZ09HakQ0bElydGlzQXhzS2xPUGN4ZXlwQTdyRThJSHZCa25KMlJiOG0wYU5JNl9wUDlzbldzWTFKR0d2UWxTUm1nT3VGOD00RDcyRkY5Mw=='

class JIRATools():
    
    @tool("Get JIRA ticket")
    def get_ticket(issueKey: str) -> str:
        """Used to retrieve the details for a JIRA ticket"""
        print("+++++++++++++++++++++ GETTING A TICKET ++++++++++++++++++++++++++")
        print(issueKey)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        headers = {
          'Authorization': JIRA_AUTH_KEY,
          'Content-Type': 'application/json'
        }
        apiConnection.request("GET", "/rest/api/3/issue/{issueKey}", headers)
        res = apiConnection.getresponse()
        return res

    @tool("Update JIRA ticket")
    def update_ticket(issueKey: str, title: str, description: str) -> str:
        """Used to update the details for a JIRA ticket"""
        print("+++++++++++++++++++++ UPDATING A TICKET ++++++++++++++++++++++++++")
        print(issueKey)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        payload = json.dumps({
          "fields": {
            "project": {
              "key": "KAN"
            },
            "summary": title,
            "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": description
                    }
                  ]
                }
              ]
            },
            "issuetype": {
              "name": "Task"
            }
          }
        })
        headers = {
          'Authorization': JIRA_AUTH_KEY,
          'Content-Type': 'application/json'
        }
        apiConnection.request("PUT", "/rest/api/3/issue/"+str(issueKey), payload, headers)
        res = apiConnection.getresponse()
        return issueKey

    @tool("Create JIRA ticket")
    def create_ticket(title: str, description: str) -> str:
        """Used to create tickets in JIRA"""
        print("+++++++++++++++++++++ OPENING A TICKET ++++++++++++++++++++++++++")
        print(title)
        print(description)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        payload = json.dumps({
          "fields": {
            "project": {
              "key": "KAN"
            },
            "summary": title,
            "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": description
                    }
                  ]
                }
              ]
            },
            "issuetype": {
              "name": "Task"
            }
          }
        })
        headers = {
          'Authorization': JIRA_AUTH_KEY,
          'Content-Type': 'application/json'
        }
        apiConnection.request("POST", "/rest/api/3/issue", payload, headers)
        res = apiConnection.getresponse()
        data = json.loads(res.read().decode())
        print(data)
        return data['key']
    
    @tool("Create JIRA subtask")
    def create_subtask(title: str, description: str, parentID: str) -> str:
        """Used to create subtasks in JIRA"""
        print("+++++++++++++++++++++ OPENING A SUBTASK ++++++++++++++++++++++++++")
        print(title)
        print(description)
        print(parentID)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        payload = json.dumps({
          "fields": {
            "project": {
              "key": "KAN"
            },
            "parent": {
              "key": parentID
            },
            "summary": title,
            "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": description
                    }
                  ]
                }
              ]
            },
            "issuetype": {
              "name": "Subtask"
            }
          }
        })
        headers = {
          'Authorization': JIRA_AUTH_KEY,
          'Content-Type': 'application/json'
        }
        apiConnection.request("POST", "/rest/api/3/issue", payload, headers)
        res = apiConnection.getresponse()
        data = json.loads(res.read().decode())
        print(data)
        return data['key']
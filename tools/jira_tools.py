import json

import http.client
from crewai_tools import tool

JIRA_AUTH_KEY='Basic Y29ubm9ydmFsYW5AZ21haWwuY29tOkFUQVRUM3hGZkdGMEc4X1dkVXNTVDFFWVB5TnFkUW1zT2l6d2FVWGZIN05FZ0I3Qm5RX2tUX25jZkNQTGoyZkdaWkZjMG4wSmphUVByMXViczR4YkFFNlh3YkxudkV0ZDk0Y0JMMG9CNDkyd1lzY1ZuZ09HakQ0bElydGlzQXhzS2xPUGN4ZXlwQTdyRThJSHZCa25KMlJiOG0wYU5JNl9wUDlzbldzWTFKR0d2UWxTUm1nT3VGOD00RDcyRkY5Mw=='

class JIRATools():

    @tool("Get JIRA ticket")
    def get_ticket(issueKey: str) -> str:
        """Used to retrieve the details for a JIRA ticket, given a Jira Key. Returns the description of the ticket"""
        print("+++++++++++++++++++++ GETTING A TICKET ++++++++++++++++++++++++++")
        print(issueKey)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        headers = {
          'Authorization': JIRA_AUTH_KEY,
          'Content-Type': 'application/json'
        }
        apiConnection.request("GET", f"/rest/api/3/issue/{issueKey}", headers=headers)
        res = apiConnection.getresponse()
        data = json.loads(res.read().decode())
        print(data['fields']['description'])
        return data['fields']['description']

    @tool("Update JIRA ticket")
    def update_ticket(issueKey: str, description: str) -> str:
        """Used to update the details for a JIRA ticket, given a Jira Key, a title, and description. Simply returns the issue key."""
        print("+++++++++++++++++++++ UPDATING A TICKET ++++++++++++++++++++++++++")
        print(issueKey)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        payload = json.dumps({
          "fields": {
            "project": {
              "key": "KAN"
            },
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
          }
        })
        headers = {
          'Authorization': JIRA_AUTH_KEY,
          'Content-Type': 'application/json'
        }
        apiConnection.request("PUT", f"/rest/api/3/issue/{issueKey}", payload, headers)
        res = apiConnection.getresponse()
        return issueKey

    @tool("Create JIRA ticket")
    def create_ticket(title: str, description: str) -> str:
        """Used to create tickets in JIRA. Responds with a Jira Key that can be used to query the Jira API in the future."""
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
        """Used to create subtasks in JIRA. Requires title, description, and the Jira Key of the parent Story."""
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
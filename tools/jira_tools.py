import json
import os

import http.client
from crewai_tools import tool

class JIRATools():
    
    @tool("Get JIRA ticket")
    def get_ticket(issueKey: str) -> str:
        """Used to retrieve the details for a JIRA ticket"""
        print("+++++++++++++++++++++ GETTING A TICKET ++++++++++++++++++++++++++")
        print(issueKey)
        apiConnection = http.client.HTTPSConnection("connorvalan.atlassian.net")
        headers = {
          'Authorization': os.environ["JIRA_AUTH_KEY"],
          'Content-Type': 'application/json'
        }
        apiConnection.request("GET", "/rest/api/3/issue/{issueKey}", headers)
        res = apiConnection.getresponse()
        return res

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
          'Authorization': os.environ["JIRA_AUTH_KEY"],
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
          'Authorization': os.environ["JIRA_AUTH_KEY"],
          'Content-Type': 'application/json'
        }
        apiConnection.request("POST", "/rest/api/3/issue", payload, headers)
        res = apiConnection.getresponse()
        data = json.loads(res.read().decode())
        print(data)
        return data['key']
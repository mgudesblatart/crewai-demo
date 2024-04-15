import json
import os

import http.client
from langchain.tools import tool

class SearchTools():

  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet
    about a a given topic and return relevant results"""
    top_result_to_return = 4
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
      "q": query
    })
    headers = {
      'X-API-KEY': os.environ["SERPER_API_KEY"],
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode())
    # check if there is an organic key
    if 'organic' not in data:
      return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
    else:
      results = data['organic']
      string = []
      for result in results[:top_result_to_return]:
        try:
          string.append('\n'.join([
              f"Title: {result['title']}", f"Link: {result['link']}",
              f"Snippet: {result['snippet']}", "\n-----------------"
          ]))
        except KeyError:
          next

      return '\n'.join(string)

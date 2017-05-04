import os
from googleapiclient.discovery import build

class google_solution(object):
    def __init__(self):
        self.my_api_key = os.environ["my_api_key"]
        self.my_cse_id = os.environ["my_cse_id"]
    
    def google_search(self, search_term, **kwargs):
        service = build("customsearch", "v1", developerKey=self.my_api_key)
        res = service.cse().list(q=search_term, cx=self.my_cse_id, **kwargs).execute()
        if "itesms" in res:
            return res['items']
        else:
            return []

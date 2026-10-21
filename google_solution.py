"""Google Custom Search JSON API, restricted by whatever CSE id is configured.

The 2017 README aimed this at the sjsu.edu domain. That restriction lived in
the Custom Search Engine settings, not in this file. The API is optional:
missing keys or a failed call produce an empty list so the greensheet answer
still goes out. This does not call a different search product.
"""

from settings import setting


class google_solution(object):
    def __init__(self):
        self.my_api_key = setting("my_api_key", "GOOGLE_API_KEY")
        self.my_cse_id = setting("my_cse_id", "GOOGLE_CSE_ID")

    def google_search(self, search_term, **kwargs):
        if not self.my_api_key or not self.my_cse_id:
            return []
        try:
            from googleapiclient.discovery import build

            service = build("customsearch", "v1", developerKey=self.my_api_key)
            res = service.cse().list(q=search_term, cx=self.my_cse_id, **kwargs).execute()
        except Exception as exc:
            print("Google Custom Search unavailable: %s" % exc)
            return []
        if isinstance(res, dict) and "items" in res:
            return res["items"]
        return []

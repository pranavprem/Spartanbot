"""IBM Watson Natural Language Classifier client.

Watson NLC on Bluemix was retired on 8 August 2022. Instances that still
existed were deleted. This module does not switch to Natural Language
Understanding or another classifier. When credentials are absent, or the
original classify endpoint fails, ``classify`` returns an empty string and
the rest of the bot continues.
"""

import requests

from settings import setting

_CLASSIFY_URL = (
    "https://gateway.watsonplatform.net/natural-language-classifier/api"
    "/v1/classifiers/{classifier_id}/classify"
)


class nlc_module(object):
    def __init__(self):
        self.username = setting("bluemix_username", "WATSON_USERNAME")
        self.password = setting("bluemix_password", "WATSON_PASSWORD")
        self.classifier_id = setting("WATSON_CLASSIFIER_ID")

    def classify(self, sentence):
        if not self.username or not self.password or not self.classifier_id:
            return ""
        url = _CLASSIFY_URL.format(classifier_id=self.classifier_id)
        try:
            response = requests.post(
                url,
                json={"text": sentence},
                auth=(self.username, self.password),
                timeout=8,
            )
            response.raise_for_status()
            classes = response.json()
            if classes["classes"][0]["confidence"] >= 0.5:
                return classes["top_class"]
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
            print("Watson NLC unavailable (the service was retired in 2022): %s" % exc)
            return ""
        return ""

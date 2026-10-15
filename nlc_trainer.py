"""Write greensheet rows out as the CSV Watson NLC used for training.

The old trainer opened a second database named ``SpartanData``, which the
learner never wrote, so the file came out empty. It now reads the same store
as the rest of the bot. The service that consumed the file is retired; the
export remains so the original training step can still be inspected.
"""

import csv


class nlc_trainer(object):
    def __init__(self, dbclient=None):
        if dbclient is None:
            from db import spartandb

            dbclient = spartandb()
        self.dbclient = dbclient

    def train(self, path="training-data.csv"):
        with open(path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            for data in self.dbclient.read():
                sentence = (data.get("sentence") or "").replace("\n", " ")
                for keyword in data.get("keywords", []):
                    writer.writerow([keyword, sentence])
        return path

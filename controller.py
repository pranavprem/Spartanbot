"""Choose a reply: remembered correction, small talk, arithmetic, or greensheet.

Google Custom Search hits are appended only when that call returns something.
Watson NLC stays off. It was disabled in 2017 after the Bluemix credentials
expired, and IBM retired the service on 8 August 2022.
"""

from calculator import calculator
from chatbot_solutions import chatbot_solutions
from custom_solution import custom_solution
from db_collection import db_collection
from google_solution import google_solution


class controller(object):
    def __init__(self):
        self.db_mode_flag = False
        self.calculation = calculator()
        self.custom_sol = custom_solution()
        self.google_sol = google_solution()
        self.collection = db_collection()
        self.chatterbot = chatbot_solutions()

    def find_solution(self, command):
        response = ""
        command = (command or "").strip().lower()
        print(command)
        print(self.db_mode_flag)
        if self.db_mode_flag is True:
            self.collection.insertCollection(command)
            response = "I'll remember that"
            self.db_mode_flag = False
        elif command == "no":
            self.db_mode_flag = True
            response = "Please enter what you consider a valid response"
        else:
            response = str(self.chatterbot.chatbot_response(command))
            if response != "":
                return response
            if command.startswith("do"):
                response = self.calculation.calculate(command)
            else:
                try:
                    custom = self.custom_sol.doCustom(command)
                except LookupError as exc:
                    custom = str(exc)
                response = "CUSTOM SOLUTION :: " + custom + "\n"
                nlc_response = ""
                if nlc_response != "":
                    response = response + "NLC SOLUTION :: \n" + nlc_response + "\n"
                response = response + "Additionally, this might help:\n"
                for hit in self.google_sol.google_search(command, num=1):
                    if not isinstance(hit, dict):
                        continue
                    response = (
                        response
                        + hit.get("formattedUrl", "")
                        + "\n"
                        + hit.get("snippet", "")
                        + "\n"
                    )
        if self.db_mode_flag is False and response != "I'll remember that":
            if response and not response.endswith("\n"):
                response = response + "\n"
            response = response + "Are you satisfied with that response?"
        return response

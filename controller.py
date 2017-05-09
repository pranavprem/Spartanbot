from calculator import calculator
from custom_solution import custom_solution
from google_solution import google_solution
from nlc_module import nlc_module
from db_collection import db_collection

class controller(object):
    def __init__(self):
        self.db_mode_flag = False
        self.calculation = calculator()
        self.custom_sol = custom_solution()
        self.google_sol = google_solution()
        self.nlc_mod = nlc_module()
        self.collection = db_collection()

    def find_solution(self, command):
        response = ""
        print command
        print self.db_mode_flag
        if self.db_mode_flag is True:
            self.collection.insertCollection(command)
            response = "I'll remember that"
            self.db_mode_flag = False
        else:
            if command == "no":
                self.db_mode_flag = True
                response = "Please enter what you consider a valid response"
            else:
                if command.startswith("do"):
                    response = self.calculation.calculate(command)
                else:
                    response = "CUSTOM SOLUTION :: " +self.custom_sol.doCustom(command) + "\n"
                    nlc_response = self.nlc_mod.classify(command)
                    if nlc_response != "":
                        response = response + "NLC SOLUTION :: \n" + nlc_response +"\n"
                    response = response + "Additionally, this might help:\n"
                for hit in self.google_sol.google_search(command, num=5):
                    response = response + hit["formattedUrl"]+"\n"+hit["snippet"]+"\n"
        if self.db_mode_flag is False and response != "I'll remember that":
            response = response + "Are you satisfied with that response?"
        return response

"""
module does calculator operations. Made in order to test bot.
"""
class calculator(object):
    def __init__(self):
        pass


    def calculate(self, command):
        operation = command.split(" ")[1:]
        if operation[1] == "+":
            return "result is %d"%(int(operation[0])+int(operation[2]))
        elif operation[1] == "-":
            return "result is %d"%(int(operation[0])-int(operation[2]))
        elif operation[1] == "*":
            return "result is %d"%(int(operation[0])*int(operation[2]))
        elif operation[1] == "/":
            return "result is %d"%int(int(operation[0])/int(operation[2]))
        else:
            return "invalid operation"

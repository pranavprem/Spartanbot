"""Tiny arithmetic commands, used to exercise the bot.

The Slack command is ``do 2 + 2``. Operators are +, -, *, and /.
"""


class calculator(object):
    def calculate(self, command):
        operation = command.split(" ")[1:]
        if len(operation) != 3:
            return "invalid operation"
        left, operator, right = operation
        try:
            first = int(left)
            second = int(right)
        except ValueError:
            return "invalid operation"
        if operator == "+":
            result = first + second
        elif operator == "-":
            result = first - second
        elif operator == "*":
            result = first * second
        elif operator == "/":
            if second == 0:
                return "invalid operation"
            result = int(first / second)
        else:
            return "invalid operation"
        return "result is %d" % result

class Rule(object):
    """
        abstract class for all the rules
        every (name, output) pair of the rule define a type of edge,
        create all the edges as instance variables and update the edge based on the output of the classify method

        to create new rule:
        1. create a new .py file and inherit the Rule class
        2. define the rule name and instanitate the edge variables
        3. overwrite the classify method, which return name + "_" + output

    """
    def __init__(self):
        self.name = ""

    def classify(self, vertex):
        pass



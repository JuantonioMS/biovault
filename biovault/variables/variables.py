import json

from biovault.variable.variable import Variable


class Variables:


    def __init__(self, *variableFiles, **kwargs) -> None:

        self.variables = self.extractVariables(*variableFiles)



    def extractVariables(self, *variableFiles) -> list:

        #from biovault.variable import Variable

        variables = []
        for variableFile in variableFiles:

            with open(variableFile, "r") as jsonFile:
                jsonInfo = json.load(jsonFile)

            for variable in jsonInfo["variables"]:
                variables.append(Variable(variable).getSpecificVariable())

        return variables



    def __iter__(self):
        return iter(self.variables)
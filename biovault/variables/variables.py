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

            generalJsonInfo = jsonInfo["general"]


            for variable in jsonInfo["variables"]:

                #  description.type
                try:

                    if not "type" in variable["description"]:
                        variable["description"]["type"] = generalJsonInfo["description"]["type"]

                except KeyError: pass

                #  info.groups
                try:

                    if not "groups" in variable["info"]:
                        variable["info"]["groups"] = generalJsonInfo["info"]["groups"]
                    else:
                        variable["info"]["groups"] = variable["info"]["groups"] + generalJsonInfo["info"]["groups"]

                except KeyError: pass

                #  source.file
                try:

                    if not "file" in variable["source"]:
                        variable["source"]["file"] = generalJsonInfo["source"]["file"]

                except KeyError: pass

                #  source.sheet
                try:

                    if not "sheet" in variable["source"]:
                        variable["source"]["sheet"] = generalJsonInfo["source"]["sheet"]

                except KeyError: pass

                #  source.format
                try:

                    if not "format" in variable["source"]:
                        variable["source"]["format"] = generalJsonInfo["source"]["format"]

                except KeyError: pass

                variables.append(Variable(variable).getSpecificVariable())

        return variables



    def __iter__(self):
        return iter(self.variables)
from os import getcwd
from bs4 import BeautifulSoup
from CustomExceptions import EmailTypeNotSupported
from Constants import EMAILTYPES
from .LoaderHelpers import getProjectRootDir

class EmailTemplateLoader:
    def __init__(self, emailType):
        self.template = ""
        self.emailType = emailType
    def loadTemplate(self, path):
        """
        Opens and loads a html template file from disk
        For now, we only support Single Column Email template
        """
        rootDir = getProjectRootDir()
        path = f'{rootDir}\{path}'

        if self.emailType == EMAILTYPES['html']:
            with open(path, "r") as htmlFile:
                self.template = BeautifulSoup(htmlFile, "html.parser")
            return self.template
        else:
            raise EmailTypeNotSupported

import random
from os import walk, getcwd

from CustomExceptions import NoFilesInNotesDir
from Constants import NOTES_DIR

class FileLoader:
    @staticmethod
    def getRandomFileToExtractNotesFrom(dirPath):
        """
        Returns a randomly chosen file name from ./notes dir.
        If no file found, raises an exception.
        """

        path = f'{getcwd()}\{dirPath}'
        (_, _, filenames) = next(walk(path))
        
        if len(filenames) < 1:
            raise NoFilesInNotesDir

        randomlyChosenFile = random.choice(filenames)
        filePath = f"{getcwd()}/{NOTES_DIR}{randomlyChosenFile}"
        
        return filePath





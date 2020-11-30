import random
from os import walk

from CustomExceptions import NoFilesInNotesDir
from Constants import NOTES_DIR

class FileLoader:
    @staticmethod
    def getRandomFileToExtractNotesFrom(dirPath):
        """
        Returns a randomly chosen file name from ./notes dir.
        If no file found, raises an exception.
        """
        (_, _, filenames) = next(walk(dirPath))
        
        if len(filenames) < 1:
            raise NoFilesInNotesDir

        randomlyChosenFile = random.choice(filenames)
        filePath = f"{NOTES_DIR}{randomlyChosenFile}"

        return filePath





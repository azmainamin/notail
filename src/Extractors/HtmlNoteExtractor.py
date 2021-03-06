import random
from .NoteExtractor import NoteExtractorInterface
from bs4 import BeautifulSoup

class HtmlNoteExtractor(NoteExtractorInterface):
    def __init__(self, filePath):
        with open(filePath, "r") as noteFile:
            self.noteBody = noteFile.read()

    def getRandomlyChosenNotes(self, numToReturn=3):
        """
        Returns a randomly selected number (based on the numToReturn arg) of 
        notes/highlights from the collection of notes (self.noteBody)
        """
        allNoteText = self._getAllNoteTexts()
        
        if len(allNoteText) < numToReturn:
            return allNoteText
        else:
            randomlyChosenNotes = []
            for _ in range(numToReturn):
                note = random.choice(allNoteText)
                randomlyChosenNotes.append(note)
                allNoteText.remove(note)
            return randomlyChosenNotes
        
    def _getAllNoteTexts(self):
        soup = BeautifulSoup(self.noteBody, "html.parser")
        tags = soup.find_all("div", class_="noteText")
        return [tag.text for tag in tags]
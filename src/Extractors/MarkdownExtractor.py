import random
import markdown
from functools import reduce
from bs4 import BeautifulSoup,Tag

from .NoteExtractor import NoteExtractorInterface

class MarkdownNoteExtractor(NoteExtractorInterface):
    def __init__(self, filePath):
        with open(filePath, "r", encoding='utf8') as noteFile:
            text = noteFile.read()
        # convert md to html
        self.noteBody = markdown.markdown(text)

    def getRandomlyChosenNotes(self, numToReturn):
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
        h2_tags = soup.find_all("h2")
        all_notes = []
        for header in h2_tags:
            results = []
            next_node = header
            while True:
                next_node = next_node.nextSibling

                if next_node is None:
                    break
                if isinstance(next_node, Tag):
                    name = next_node.name 
                    if name == 'h2':
                        break
                    if "```" in next_node.contents[0]:
                        code_tag = BeautifulSoup().new_tag('code')
                        code_tag.append(next_node.contents[0])
                        results.append(code_tag)
                    if name == 'p' or name == 'ul':
                        results.append(next_node)
            reduced = self._appendTags(results)
            all_notes.append(reduced)
    
        return all_notes 

    def _appendTags(self, results):
        if len(results) > 1:
            first = BeautifulSoup().new_tag('div')
            for tag in results:
                first.append(tag)
                BeautifulSoup().new_tag('br')
        return first     
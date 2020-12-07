import random
from typing import List, Tuple
import fitz  # install with 'pip install pymupdf'

from .NoteExtractor import NoteExtractorInterface

class PdfNotesExtractor(NoteExtractorInterface):
    def __init__(self, filePath):
        self.noteBody = fitz.open(filePath)
    
    def getRandomlyChosenNotes(self, numToReturn=3):
        """
        Returns a randomly selected number (based on the numToReturn arg) of 
        notes/highlights from the collection of notes (self.noteBody)
        """
        allNotes = self._getAllHighlights()

        if len(allNotes) < numToReturn:
            return allNotes
        else:
            result = []
            for _ in range(numToReturn):
                note = random.choice(allNotes)
                result.append(note)
                allNotes.remove(note)
   
    def _getAllHighlights(self):
        highlights = []
        for page in self.noteBody:
            highlights += self._handle_page(page)

        return highlights

    def _handle_page(self, page):
        wordlist = page.getText("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        highlights = []
        annot = page.firstAnnot
        while annot:
            # annot.type == 8 means its a highlight: 
            # https://pymupdf.readthedocs.io/en/latest/vars.html#annotationtypes
            if annot.type[0] == 8:
                highlights.append(self._parse_highlight(annot, wordlist))
            annot = annot.next
        return highlights

    def _parse_highlight(self, annot, wordlist):
        points = annot.vertices
        # find how many quadrilaterals are in the doc
        quad_count = int(len(points) / 4)
        sentences = []
        for i in range(quad_count):
            # where the highlighted part is by intersecting
            # the rectangles
            r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect
            words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
            sentences.append(" ".join(w[4] for w in words))
        sentence = " ".join(sentences)
        return sentence 
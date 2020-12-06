from dotenv import load_dotenv
import time

from Loaders.FileLoader import FileLoader
from Extractors.ExtractorFactory import ExtractorFactory
from Extractors.HtmlNoteExtractor import HtmlNoteExtractor
from Loaders.EmailTemplateLoader import EmailTemplateLoader
from Email.EmailGenerator import EmailGenerator
from Email.EmailSender import EmailSender
from Constants import NOTES_DIR, DEFAULT_NUM_OF_NOTES, EMAIL_TEMPLATE_DIR, EMAILTYPES
    
from typing import List, Tuple

import fitz  # install with 'pip install pymupdf'

def main():
    #load env variables
    load_dotenv(verbose=True)
    # register extractors
    extractorFactory = ExtractorFactory()
    extractorFactory.registerExtractor(EMAILTYPES['html'], HtmlNoteExtractor)
    
    randomlyChosenFile = FileLoader.getRandomFileToExtractNotesFrom(NOTES_DIR)

    # load file
    with open(randomlyChosenFile, "r") as noteFile:
        page = noteFile.read()
        #TODO: Get the extension of the file programmatically
        fileType = EMAILTYPES['html'] 
        Extractor = extractorFactory.getExtractor(fileType)
        noteExtractor = Extractor(page)
        randomlyChosenNotes = noteExtractor.getRandomlyChosenNotes(DEFAULT_NUM_OF_NOTES)
    
    # TODO: More than one template
    templateLoader = EmailTemplateLoader(EMAILTYPES['html'])
    template = templateLoader.loadTemplate(EMAIL_TEMPLATE_DIR)
    
    emailGenerator = EmailGenerator()
    emailBody = emailGenerator.createEmailBody(template, randomlyChosenNotes)
    
    emailSender = EmailSender(EMAILTYPES['html'])
    #emailSender.sendEmail(emailBody)
    
    # CMD Display
    print("Email Sent")
    time.sleep(2)

def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence


def handle_page(page):
    wordlist = page.getText("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights


def extractPDF(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights
    
if __name__ == "__main__":
    main()
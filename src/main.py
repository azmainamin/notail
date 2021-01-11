from dotenv import load_dotenv
import time
from bs4 import BeautifulSoup, NavigableString, Tag

from Loaders.FileLoader import FileLoader
from Extractors.ExtractorFactory import ExtractorFactory
from Extractors.HtmlNoteExtractor import HtmlNoteExtractor
from Extractors.PdfNotesExtractor import PdfNotesExtractor
from Loaders.EmailTemplateLoader import EmailTemplateLoader
from Email.EmailGenerator import EmailGenerator
from Email.EmailSender import EmailSender
from Constants import NOTES_DIR, DEFAULT_NUM_OF_NOTES, EMAIL_TEMPLATE_DIR, FILETYPES

def main():
    #load env variables
    load_dotenv(verbose=True)
    mdTest()
    # register extractors
"""     extractorFactory = ExtractorFactory()
    extractorFactory.registerExtractor(FILETYPES['html'], HtmlNoteExtractor)
    extractorFactory.registerExtractor(FILETYPES['pdf'], PdfNotesExtractor)
    
    # load file
    randomlyChosenFile = FileLoader.getRandomFileToExtractNotesFrom(NOTES_DIR)
    fileType = randomlyChosenFile.split('.')[1]
    Extractor = extractorFactory.getExtractor(fileType)
    noteExtractor = Extractor(randomlyChosenFile)
    randomlyChosenNotes = noteExtractor.getRandomlyChosenNotes(DEFAULT_NUM_OF_NOTES)
    # email
    templateLoader = EmailTemplateLoader(FILETYPES['html'])
    template = templateLoader.loadTemplate(EMAIL_TEMPLATE_DIR)
    
    emailGenerator = EmailGenerator()
    emailBody = emailGenerator.createEmailBody(template, randomlyChosenNotes)
    
    emailSender = EmailSender(FILETYPES['html'])
    #emailSender.sendEmail(emailBody) """
    
    # CMD Display
    
def mdTest():
    with open("../data/notes/ds.html", "r", encoding='utf8') as file:
        text = file.read()
    soup = BeautifulSoup(text, "html.parser")
    tags = soup.find_all("h2")
    for header in tags:
        results = []
        next_node = header
        while True:
            next_node = next_node.nextSibling
            if next_node is None:
                break
            if isinstance(next_node, Tag):
                if next_node.name == 'h2' or next_node.name == 'h3':
                    break
                if next_node.name == 'p':
                    results.append(next_node.text)
                if next_node.name == 'pre':
                    results.append(next_node)
        print("NOTES: ")
        print(",".join(results))

if __name__ == "__main__":
    main()
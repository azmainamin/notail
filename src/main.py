from dotenv import load_dotenv
import time
from bs4 import BeautifulSoup, NavigableString, Tag

from Loaders.FileLoader import FileLoader
from Extractors.ExtractorFactory import ExtractorFactory
from Extractors.HtmlNoteExtractor import HtmlNoteExtractor
from Extractors.PdfNotesExtractor import PdfNotesExtractor
from Extractors.MarkdownExtractor import MarkdownNoteExtractor
from Loaders.EmailTemplateLoader import EmailTemplateLoader
from Email.EmailGenerator import EmailGenerator
from Email.EmailSender import EmailSender
from Constants import NOTES_DIR, DEFAULT_NUM_OF_NOTES, EMAIL_TEMPLATE_DIR, FILETYPES

def main():
    #load env variables
    load_dotenv(verbose=True)
    # register extractors
    extractorFactory = ExtractorFactory()
    extractorFactory.registerExtractor(FILETYPES['html'], HtmlNoteExtractor)
    extractorFactory.registerExtractor(FILETYPES['pdf'], PdfNotesExtractor)
    extractorFactory.registerExtractor(FILETYPES['markdown'], MarkdownNoteExtractor)
    
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
    emailSender.sendEmail(emailBody)
    
    # CMD Display
    print("Email Sent")
    time.sleep(2)
    
if __name__ == "__main__":
    main()
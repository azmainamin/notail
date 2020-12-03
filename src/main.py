from dotenv import load_dotenv
import time

from Loaders.FileLoader import FileLoader
from Extractors.ExtractorFactory import ExtractorFactory
from Extractors.HtmlNoteExtractor import HtmlNoteExtractor
from Loaders.EmailTemplateLoader import EmailTemplateLoader
from Email.EmailGenerator import EmailGenerator
from Email.EmailSender import EmailSender
from Constants import NOTES_DIR, DEFAULT_NUM_OF_NOTES, EMAIL_TEMPLATE_DIR, EMAILTYPES
    
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
    emailSender.sendEmail(emailBody)
    
    # CMD Display
    print("Email Sent")
    time.sleep(2)

if __name__ == "__main__":
    main()
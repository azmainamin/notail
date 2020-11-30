import copy
from bs4 import BeautifulSoup

class EmailGenerator:
    def createEmailBody(self, template, randomlyChosenNotes):
        """
        Generates a html email with notes to review
        """
        textContainer = template.find(id='text-container')

        for note in randomlyChosenNotes:
            textContainer = self._createBodyTagsForEachNote(template, note)
    
        template.find(id='text-container').replaceWith(textContainer)
        
        return str(template)

    def _createBodyTagsForEachNote(self, template, note):
        """
        Creates the html tag for each note i.e. <div>NOTE_TO_REVIEW</div>
        """
        textContainer = template.find(id='text-container')
        textBody = template.findAll('div', {"class" : "body-text"})
        copy_tag = copy.copy(textBody[0])
        copy_tag.string = note
        # TODO: extract to named functions
        copy_tag.append(BeautifulSoup().new_tag('br'))
        copy_tag.append(BeautifulSoup().new_tag('br'))
        copy_tag.append(BeautifulSoup().new_tag('hr'))
        textContainer.div.insert_after(copy_tag)

        return textContainer
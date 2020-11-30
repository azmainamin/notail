class NoFilesInNotesDir(Exception):
    """
    Raised when there are no files in the notes dir
    """
    pass

class EmailTypeNotSupported(Exception):
    """
    Raised when email template is not supported. 
    """
    pass
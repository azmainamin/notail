class ExtractorFactory:
    def __init__(self):
        self._extractors = {}

    def getExtractor(self, fileType):
        """
        Returns the extractor based on filetype i.e. for a html doc,
        a html extractor will be returned
        """
        extractor = self._extractors[fileType]
        if extractor is None:
            print("FileType not supported yet")
        
        return extractor

    def registerExtractor(self, fileType, extractor):
        """
        Adds an extractor to a filetype as a key-value pair 
        """
        self._extractors[fileType] = extractor
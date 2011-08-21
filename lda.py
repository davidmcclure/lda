import re

class Document(object):

    '''
    Splits a text file into an ordered list of words.
    '''

    # List of punctuation characters to scrub. Omits, the single apostrophe,
    # which is handled separately so as to retain contractions.
    PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']

    # Carriage return strings, on *nix and windows.
    CARRIAGE_RETURNS = ['\n', '\r\n']

    # Final sanity-check regex to run on words before they get
    # pushed onto the core words list.
    WORD_REGEX = "^[a-z']+$"

    def __init__(self, filepath):
        '''
        Set source file location, build contractions list, and
        initialize empty lists for lines and words.
        '''
        self.filepath = filepath
        self.file = open(self.filepath)
        self.lines = []
        self.words = []

    def split(self):
        '''
        Split file into an ordered list of words. Scrub out
        punctuation; lowercase everything; preserve contractions;
        disallow strings that include non-letters.
        '''
        self.lines = [line for line in self.file]
        for line in self.lines:
            words = line.split(' ')
            for word in words:
                clean_word = self._clean_word(word)
                if clean_word:
                    self.words.append(clean_word)

    def _clean_word(self, word):
        '''
        Parses a space-delimited string from the text and determines
        whether or not it is a valid word. Scrubs punctuation, retains
        contraction apostrophes. If cleaned word passes final regex,
        returns the word; otherwise, returns None.
        '''
        word = word.lower()
        for punc in Document.PUNCTUATION + Document.CARRIAGE_RETURNS:
            word = word.replace(punc, '').strip("'")
        return word if re.match(Document.WORD_REGEX, word) else None


class Corpus(object):

    '''
    A collection of documents.
    '''

    def __init__(self):
        '''
        Initialize empty document list.
        '''
        self.documents = []

    def add_document(self, document):
        '''
        Add a document (Document instantiation) to the corpus.
        '''
        self.documents.append(document)

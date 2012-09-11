import re
import numpy as np
from utils import choose

"""
Author: 
davidmcclure (https://github.com/davidmcclure)
Alex Kong (https://github.com/hitalex)

Reference:
Gibbs sampling update
@article{heinrich2005parameter,
  title={Parameter estimation for text analysis},
  author={Heinrich, G.},
  journal={Web: http://www.arbylon.net/publications/text-est.pdf},
  year={2005}
}
"""

np.set_printoptions(threshold='nan')

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
        Set source file location, build contractions list, and initialize empty
        lists for lines and words.
        '''
        self.filepath = filepath
        self.file = open(self.filepath)
        self.lines = []
        self.words = []


    def split(self, STOP_WORDS_SET):
        '''
        Split file into an ordered list of words. Scrub out punctuation;
        lowercase everything; preserve contractions; disallow strings that
        include non-letters.
        '''
        self.lines = [line for line in self.file]
        for line in self.lines:
            words = line.split(' ')
            for word in words:
                clean_word = self._clean_word(word)
                if clean_word and (clean_word not in STOP_WORDS_SET) and (len(clean_word) > 1): # omit stop words
                    self.words.append(clean_word)


    def _clean_word(self, word):
        '''
        Parses a space-delimited string from the text and determines whether or
        not it is a valid word. Scrubs punctuation, retains contraction
        apostrophes. If cleaned word passes final regex, returns the word;
        otherwise, returns None.
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
        Add a document to the corpus.
        '''
        self.documents.append(document)


    def build_vocabulary(self):
        '''
        Construct a list of unique words in the corpus.
        '''
        # ** ADD ** #
        # exclude words that appear in 90%+ of the documents
        # exclude words that are too (in)frequent
        discrete_set = set()
        for document in self.documents:
            for word in document.words:
                discrete_set.add(word)
        self.vocabulary = list(discrete_set)
        


    def lda(self, number_of_topics, iterations, alpha, beta):

        '''
        Model topics.
        '''
        print "Gibbs sampling process..."
        # Get vocabulary and number of documents.
        self.build_vocabulary()
        number_of_documents = len(self.documents)
        vocabulary_size = len(self.vocabulary)

        # Create the counter arrays.
        self.document_topic_counts = np.zeros([number_of_documents, number_of_topics], dtype=np.int)
        self.topic_word_counts = np.zeros([number_of_topics, len(self.vocabulary)], dtype=np.int)
        self.current_word_topic_assignments = []
        self.topic_counts = np.zeros(number_of_topics)

        # Initialize
        print "Initializing..."
        for d_index, document in enumerate(self.documents):
            word_topic_assignments = []
            for word in document.words:
                if word in self.vocabulary:
                    # Select random starting topic assignment for word.
                    w_index = self.vocabulary.index(word)
                    starting_topic_index = np.random.randint(number_of_topics) # randomly assign topic to every word
                    word_topic_assignments.append(starting_topic_index)
                    # Set current topic assignment, increment doc-topic and word-topic counters.
                    self.document_topic_counts[d_index, starting_topic_index] += 1
                    self.topic_word_counts[starting_topic_index, w_index] += 1
                    self.topic_counts[starting_topic_index] += 1
            self.current_word_topic_assignments.append(np.array(word_topic_assignments))

        # Run the sampler.
        for iteration in range(iterations):
            print "Iteration #" + str(iteration + 1) + "..."
            for d_index, document in enumerate(self.documents):
                for w, word in enumerate(document.words):
                    if word in self.vocabulary:
                        w_index = self.vocabulary.index(word)
                        # Get the topic that the word is currently assigned to.
                        current_topic_index = self.current_word_topic_assignments[d_index][w]
                        # Decrement counts.
                        self.document_topic_counts[d_index, current_topic_index] -= 1
                        self.topic_word_counts[current_topic_index, w_index] -= 1
                        self.topic_counts[current_topic_index] -= 1
                        # Get new topic.
                        topic_distribution = (self.topic_word_counts[:, w_index] + beta) * \
                            (self.document_topic_counts[d_index] + alpha) / \
                            (self.topic_counts + beta) # changed by hitalex
                        #new_topic_index = np.random.multinomial(1, np.random.dirichlet(topic_distribution)).argmax()
                        # choose a new topic index according to topic distribution
                        new_topic_index = choose(range(number_of_topics), topic_distribution)
                        # Reassign and notch up counts.
                        self.current_word_topic_assignments[d_index][w] = new_topic_index
                        self.document_topic_counts[d_index, new_topic_index] += 1
                        self.topic_word_counts[new_topic_index, w_index] += 1
                        self.topic_counts[new_topic_index] += 1

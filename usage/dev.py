import os
import glob
import sys
sys.path.append("/Users/davidmcclure/Projects/lda")
import lda

corpus = lda.Corpus() # instantiate corpus

# iterate over the files in the directory.
document_path = '../texts/grimm_fairy_tales'
for document_file in glob.glob(os.path.join(document_path, '*.txt')):
    document = lda.Document(document_file) # instantiate document
    document.split() # tokenize
    document.build_document_wordcount_matrix() # populate word:wordcount matrix
    corpus.add_document(document) # push onto corpus documents list

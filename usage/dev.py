import os
import glob
import sys
sys.path.append("/Users/davidmcclure/Projects/lda")

import lda

corpus = lda.Corpus()

document_path = '../texts/grimm_fairy_tales'
for document_file in glob.glob(os.path.join(document_path, '*.txt')):
    corpus.add_document(lda.Document(document_file))

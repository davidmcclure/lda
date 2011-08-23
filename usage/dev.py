import os
import glob
import sys
sys.path.append("/Users/davidmcclure/Projects/lda")
import lda

corpus = lda.Corpus() # instantiate corpus

# iterate over the files in the directory.
document_paths = ['../texts/grimm_fairy_tales', '../texts/tech_blog_posts', '../texts/nyt']
for document_path in document_paths:
    for document_file in glob.glob(os.path.join(document_path, '*.txt')):
        document = lda.Document(document_file) # instantiate document
        document.split() # tokenize
        corpus.add_document(document) # push onto corpus documents list

corpus.build_vocabulary()
print len(corpus.vocabulary)
# corpus.lda(100, 30, 2.5, 0.1)
# print corpus.topic_word_counts
# print corpus.document_topic_counts

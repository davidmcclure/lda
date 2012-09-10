import os
import glob
import sys
from operator import itemgetter # for sort
#sys.path.append("/home/kongqingchao/github/lda-with-gibbs/")
import lda

def print_topic_word_distribution(corpus, number_of_topics, topk, filepath):
    """
    Print topic-word distribution to file and list @topk most probable words for each topic
    """
    V = len(corpus.vocabulary) # size of vocabulary
    assert(topk < V)
    f = open(filepath, "w")
    for k in range(number_of_topics):
        word_count = corpus.topic_word_counts[k, :]
        word_index_count = []
        for i in range(V):
            word_index_count.append([i, word_count[i]])
        word_index_count = sorted(word_index_count, key=itemgetter(1)) # sort by word count
        f.write("Topic #" + str(k) + ":\n")
        for i in range(topk):
            [index, count] = word_index_count[i]
            f.write(corpus.vocabulary[index] + " ")
        f.write("\n")
        
    f.close()
    
def print_document_topic_distribution(corpus, number_of_topics, topk, filepath):
    """
    Print document-topic distribution to file and list @topk most probable topics for each document
    """
    assert(topk < number_of_topics)
    f = open(filepath, "w")
    D = len(corpus.documents) # number of documents
    for d in range(D):
        topic_count = corpus.document_topic_counts[d, :]
        topic_index_count = []
        for i in range(number_of_topics):
            topic_index_count.append([i, topic_count[i]])
        topic_index_count = sorted(topic_index_count, key=itemgetter(1))
        f.write("Document #" + str(d) + ":\n")
        for i in range(topk):
            [index, count] = topic_index_count[i]
            f.write("topic" + str(index) + " ")
        f.write("\n")
        
    f.close()
        
def main(argv):
    print "Usage: python ./main.py number_of_topics alpha beta maxiteration"
    corpus = lda.Corpus() # instantiate corpus
    # iterate over the files in the directory.
    document_paths = ['./texts/grimm_fairy_tales', './texts/tech_blog_posts', './texts/nyt']
    for document_path in document_paths:
        for document_file in glob.glob(os.path.join(document_path, '*.txt')):
            document = lda.Document(document_file) # instantiate document
            document.split() # tokenize
            corpus.add_document(document) # push onto corpus documents list

    corpus.build_vocabulary()
    print "Vocabulary size:" + str(len(corpus.vocabulary))
    
    number_of_topics = int(argv[1])
    alpha = float(argv[2])
    beta = float(argv[3])
    max_iterations = int(argv[4])
    corpus.lda(number_of_topics, max_iterations, alpha, beta)
    
    print_topic_word_distribution(corpus, number_of_topics, 50, "./topic-word.txt")
    
if __name__ == "__main__":
    main(sys.argv)

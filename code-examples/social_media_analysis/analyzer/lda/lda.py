import gensim
from gensim import corpora

def create_dictionary(data):
    return corpora.Dictionary(data['preprocess_text'])

def create_corpus(data, dictionary):
    return [dictionary.doc2bow(text) for text in data['preprocess_text']]

def run_model(data):
    # Create dictionary and corpus
    # You can improve the model by changing the number of topics, passes, etc.
    # You can improve the model by using n-grams
    dictionary = create_dictionary(data)
    corpus = create_corpus(data, dictionary)
    lda_model = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    topics = lda_model.print_topics(num_words=10)
    return topics
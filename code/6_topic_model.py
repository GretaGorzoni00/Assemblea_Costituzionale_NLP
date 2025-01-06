import spacy
import gensim
import os
import time
import pickle
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

start_time = time.time()

nlp = spacy.load("it_core_news_md")

def carica_corpus_spacy(directory):
    all_tokens = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                doc = nlp(content)
                tokens = [
    token.lemma_ 
    for token in doc 
    if token.lemma_ not in {"è", "più", "pr", "\n", "o", "il", "a il", "di il", "perchè", "in il", "così",} and  # parole da escludere
    not token.is_stop and 
    not token.is_punct 
]
                all_tokens.append(tokens)
               
    return all_tokens

directory_corpus = 'assemblea'
corpus = carica_corpus_spacy(directory_corpus)

dictionary = gensim.corpora.Dictionary(corpus) # mappa ogni parola con un identificatore unico
word_to_doc = [dictionary.doc2bow(doc) for doc in corpus] #bag of words
tfidf = gensim.models.TfidfModel(word_to_doc) # modello TF-IDF sui dati
corpus_tfidf = tfidf[word_to_doc]

pickle.dump(corpus_tfidf, open('models_8topic/corpus.pkl', 'wb'))
dictionary.save('models_8topic/dictionary.gensim')

print("Il dizionario è stato salvato")

num_topics = 8 # numero di topic da identiicare nel modello

ldamodel = gensim.models.ldamodel.LdaModel(word_to_doc, num_topics=num_topics, id2word=dictionary, 
                                           passes=50,iterations=150, alpha='auto', eta=0.01)
# passes = num passaggi sui dati
ldamodel.save('models_8topic/models_topic8.gensim')

topics = ldamodel.print_topics(num_words=7)
for topic in topics:
    print(topic)

dictionary_loaded = gensim.corpora.Dictionary.load('models_8topic/dictionary.gensim')
corpus_tfidf = pickle.load(open('models_8topic/corpus.pkl', 'rb'))

lda = gensim.models.ldamodel.LdaModel.load('models_8topic/nuovo_topic8.gensim')
lda_display = gensimvis.prepare(lda, corpus_tfidf, dictionary_loaded, sort_topics=False)

pyLDAvis.save_html(lda_display, 'lda_visualization_8topic.html')

end_time = time.time()
execution_time = end_time - start_time
print(f'Tempo totale di esecuzione: {execution_time:.2f} secondi')

# Tempo totale di esecuzione: 759.54 secondi = 12,6 minuti
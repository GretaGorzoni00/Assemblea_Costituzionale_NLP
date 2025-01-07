import spacy
import gensim
import os
import pickle

nlp = spacy.load("it_core_news_md")


def carica_modelli():
    dictionary = gensim.corpora.Dictionary.load('models_8topic/dictionary.gensim')
    corpus_tfidf = pickle.load(open('models_8topic/corpus.pkl', 'rb'))
    lda = gensim.models.LdaModel.load('models_8topic/models_topic8.gensim')
    return dictionary, lda


def analizza_documento(file_path, dictionary, lda):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        doc = nlp(content)
        tokens = [
            token.lemma_ 
            for token in doc 
            if token.lemma_ not in {"è", "più", "pr", "\n", "o", "il", "a il", "di il", "perchè", "in il", "così",}
            and not token.is_stop and 
            not token.is_punct 
        ]
        
    # creazione della bag of words 
    new_doc_bow = dictionary.doc2bow(tokens)
    # calcolo della distribuzione dei topic nel documento
    topic_distribution = lda.get_document_topics(new_doc_bow)
    
    # topic ordinati
    return sorted(topic_distribution, key=lambda x: x[1], reverse=True)

# funzione con cui intergaire con l'utente
def utente():
    dictionary, lda = carica_modelli()
    
    
    file_name = input("Inserisci il nome del file della relazione da analizzare (ID_DD-MM-AA_RELATORE.txt): ")
    file_path = os.path.join('assemblea', file_name)
    
    if not os.path.exists(file_path):
        print(f"Il file inserito non esiste")
        return
   
    topic_distribution_sorted = analizza_documento(file_path, dictionary, lda)
    
    # visualizzazione dei topic 
    print("\nDistribuzione dei topic nel documento:")
    for topic_id, prob in topic_distribution_sorted:
        print(f"Topic {topic_id}: Probabilità {prob:.4f}")
        words = lda.show_topic(topic_id, topn=7)
        words_list = ", ".join([word[0] for word in words])
        print(f"  Parole principali: {words_list}")


utente()
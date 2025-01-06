import os
import time
import spacy
from collections import Counter

start_time = time.time()
token_counter = Counter()

nlp = spacy.load("it_core_news_md")

cartella_corpus = "assemblea"

def tokenizza(percorso_file):
    with open(percorso_file, "r", encoding="utf-8") as file:
        testo = file.read()
        doc = nlp(testo)
        for token in doc:
                token_counter[token.text] += 1
                
for nome_file in os.listdir(cartella_corpus):
    percorso_file = os.path.join(cartella_corpus, nome_file)
    if os.path.isfile(percorso_file):
        tokenizza(percorso_file)
                
total_count = sum(token_counter.values())
print(f"Totale delle occorrenze: {total_count}")


end_time = time.time()
execution_time = end_time - start_time
print(f'Tempo totale di esecuzione: {execution_time:.2f} secondi')

# Tempo totale di esecuzione: 495.08 secondi

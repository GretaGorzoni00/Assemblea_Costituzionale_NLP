import os
import spacy
from collections import Counter
import pandas as pd
import plotly.express as px

import time
start_time = time.time()

nlp = spacy.load("it_core_news_md")
cartella_corpus = "assemblea"

# inizializazione di un oggetto counter
token_counter = Counter()

def tokenizza_e_pos_file(percorso_file):
    with open(percorso_file, "r", encoding="utf-8") as file:
        testo = file.read()
        doc = nlp(testo)
        for token in doc:
            if token.pos_ in {"VERB", "ADJ", "NOUN", "ADV"} and token.text not in {"è", "essere", "avere", "più", "pr", "\n", "o", "il", "a il", "di il", "perchè", "in il", "pr", "ha", "così", "più", "non", "anche", "ora", "quindi", "così"}:
                #incremento del conteggio del token come chiave del dizionario
                token_counter[token.text] += 1

for nome_file in os.listdir(cartella_corpus):
    percorso_file = os.path.join(cartella_corpus, nome_file)
    if os.path.isfile(percorso_file):
        tokenizza_e_pos_file(percorso_file)

token_frequenti = token_counter.most_common(20)
# most common di counter è una lista di tuple
# zip funzione che raggruppa elelmenti in base al loro indice 
# unpacking operator seprara le tuple nella lista 
token, freq = zip(*token_frequenti)

print(token_frequenti)

df = pd.DataFrame({'Wordtype': token, 'Frequenza': freq})

# colore distinto per ciascuna colonna
df['Colore'] = df['Wordtype']

fig = px.bar(df, x="Wordtype", y="Frequenza", color="Colore", 
             title="Wordtype con maggiore frequenza tra i PoS: VERB, ADJ, NOUN, ADV", 
             labels={"Wordtype": "Wordtype", "Frequenza": "Frequenza"}, text="Frequenza")

# informazioni interazione 
fig.update_traces(hovertemplate="Parola: %{x}<br>Frequenza: %{y}<extra></extra>")

fig.update_layout(showlegend=False)

output_html = "grafico_interattivo_colorato.html"
fig.write_html(output_html)

end_time = time.time()
execution_time = end_time - start_time
print(f"conferma salvataggio file HTML'{output_html}'")
print(f"Tempo totale di esecuzione: {execution_time:.2f} secondi")

# Tempo totale di esecuzione : 502.88 secondi = 8,3 minuti

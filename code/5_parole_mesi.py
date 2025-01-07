import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import plotly.graph_objects as go
import numpy as np
import time

start_time = time.time()

nlp = spacy.load("it_core_news_md")
nlp.max_length = 2000000
cartella_corpus = "assemblea"

# dizionario che associa al nome dei mesi il numero che compare nel nome dei file
# dzionario mensi_nomi funzionale a successiva sotituzione
mesi_nomi = {"03": "Marzo", "04": "Aprile", "05": "Maggio", "06": "Giugno",
    "07": "Luglio", "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"}
dizionario = defaultdict(list)
# defaultdict evita errore associando valore a una chiave che non esistente, la prima volta che si tenta di accedervi
# funzionale per usare la funzione append e inserire i testi come value dopo averli processati
mesi_ordine = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
               "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
ordine_mesi = []

def estrai_mese(nome_file):
    mese = nome_file.split('_')[1].split('-')[1]
    return mesi_nomi.get(mese, "Mese sconosciuto")

def tokenizza_file(percorso_file):
    with open(percorso_file, "r", encoding="utf-8") as file:
        testo = file.read()
        doc = nlp(testo)
        mese = estrai_mese(os.path.basename(percorso_file))
        if mese not in ordine_mesi:
            ordine_mesi.append(mese)
        tokens_validi = [token.text for token in doc 
                         if not token.is_stop 
                         and not token.is_punct 
                         and token.lemma_ not in {"è", "più", "pr", "\n", "o", "il", "a il", "di il", "perchè", "in il"}
                         and not any(char.isdigit() for char in token.lemma_)
                         and not token.text.strip() == ""]
        dizionario[mese].append(" ".join(tokens_validi))

for nome_file in os.listdir(cartella_corpus):
    percorso_file = os.path.join(cartella_corpus, nome_file)
    tokenizza_file(percorso_file)

# le relazioni di ogni mese da stringhe in una lista (valude della kay mese) a stringa unita
dizionario = {mese: " ".join(testi) for mese, testi in dizionario.items()}

# defisco una mia funzione di tokenizzazione con Spacy per utilizzarla in TfidfVectorizer
# e sostituire così il comportamento predefitnito di tokenizzazione che ho visto non essere
# ottimale in questo contesto
def identity_tokenizer(text):
    doc = nlp(text)
    return [token.text for token in doc]

# Inizializza il TfidfVectorizer
vectorizer = TfidfVectorizer(
    tokenizer=identity_tokenizer,
    lowercase=False, # da normalizzazione già lowercase
    smooth_idf=False, # per penalizzare le parole che occorrono in tutto il corpus
    sublinear_tf=True, # per penalizzare le parole in assoluto frequenti, grammaticali per la legge di Zipf
    min_df=0.05,  # frequenza minima, per evitare occasionalismi
    max_df=0.9, # frequenza massima, per evitare parole grammaticali
    norm=None # conservare i valori assoluti di TF-IDF
)

# corpus é una lista di stringhe, dove ogni stringa sono le relazioni di un mese
# vectorizer.fit_transform necessita di avere in input lista
corpus = list(dizionario.values())
tfidf_matrix = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names_out()
# parole colonne nella matrice tdidf

# disposizione dei mesi in cerchio
num_mesi = 12
theta = np.linspace(0, 2 * np.pi, num_mesi, endpoint=False)
x_coords = 10 * np.cos(theta)
y_coords = 10 * np.sin(theta)
colori = ["royalblue", "firebrick", "forestgreen", "purple", "orange", "gold", "darkcyan", "magenta", "deepskyblue"]


fig = go.Figure()

for idx, mese in enumerate(mesi_ordine):
    if mese in dizionario: # dizionario{mese:relazioni}, non in dizionario gennaio, febbraio, agosto
        mese_idx = ordine_mesi.index(mese) # lista popolata solo dai mesi con relazioni
        tfidf_scores = tfidf_matrix[mese_idx] # estrazione riga matrice = valori TF-IDF per parole delle relazioni dello specifico mese 
        sorted_items = tfidf_scores.toarray().flatten().argsort()[::-1] # valori TF-IDF delle parole decresenti

        parole_specifiche = []
        valori_TFIDF = [] # memorizzazione valori TF-IDF per mostrarli nel grafico
        for i in sorted_items[:5]: # estrazione degli indici delle 5 parole con punteggi più alti
            parola = feature_names[i] # estrazione delle parole corrisponedenti agli indici
            score = tfidf_scores[0, i]
            parole_specifiche.append(parola)
            valori_TFIDF.append(score)

        # informazioni interazione
        hover_text = "<br>".join([f"{word}: {score:.2f}" for word, score in zip(parole_specifiche, valori_TFIDF)])
        # funzione zip unione da lista A e lista B di elemento A con elemento B
        #f-string formatta valori TF-IDF con due decimali per agevolare visualizzazione
        # <br> tag HTML per interruzione 

        # coordinate della disposizione dei mesi in cerchio generate prima, fuori dal ciclo for
        fig.add_trace(go.Scatter(
            x=[x_coords[idx]], 
            y=[y_coords[idx]],
            mode='markers+text',
            marker=dict(size=50, color=colori[idx % len(colori)]),
            text=mese,
            textposition="bottom center",
            hovertemplate=f"<b>{mese}</b><br>{hover_text}<extra></extra>",
            name=mese
        ))
    else:  # mesi senza relazioni: gennaio, febbraio, agosto
        fig.add_trace(go.Scatter(
            x=[x_coords[idx]], 
            y=[y_coords[idx]],
            mode='markers+text',
            marker=dict(size=40, color='lightgrey', line=dict(color='black', width=1)),
            text=mese,
            textposition="bottom center",
            hovertemplate=f"<b>{mese}</b><br>No Data<extra></extra>",
            name=mese
        ))

# 1947, anno a cui tutti i mesi fanno riferimento 
fig.add_trace(go.Scatter(
    x=[0], 
    y=[0],
    mode='text',
    text=["1947"],
    textfont=dict(size=50, color="black"),  
    showlegend=False,
    hoverinfo="skip"  
))

fig.update_layout(
    title="1947: Le parole significative per ogni mese",
    xaxis=dict(showticklabels=False, zeroline=False),
    yaxis=dict(showticklabels=False, zeroline=False),
    plot_bgcolor="white",
    height=800,
    width=800
)

output_html = "parole_mesi.html"
fig.write_html(output_html)

print(f"conferma salvataggio file HTML {output_html}")

end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo totale di esecuzione: {execution_time:.2f} secondi")

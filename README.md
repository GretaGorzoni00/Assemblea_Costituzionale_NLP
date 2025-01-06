# Assemblea_Costituzionale_NLP

![Python](https://img.shields.io/badge/Lang-Python-blue)

Analisi con tecniche NLP e di Topic Model di un corpus rappresentativo della discussione dell’Assemblea Costituente (1947).

## Descrizione 

Il lavoro consiste in un'analisi linguistica dei discorsi dell'Assemblea Costituente italiana, svcolta a partire da un corpus rappresentativo del dibattito parlamentare relativo alla discussione della Costituzione italiana. Le relazioni dell'Assemblea costituente si svolgono tra marzo 1947 e dicembre 1947. Il presente progetto mira a sviluppare una modalità di analisi interdisciplinare che si possa applicare alle fonti storiche di questo tipo. L'obiettivo del progetto è quello di esplorare il lessico e i temi prevalenti nei discorsi dei membri dell'Assemblea, utilizzando tecniche di elaborazione del linguaggio naturale (NLP) e Topic Modelling. L'analisi è stata realizzata tramite un flusso di lavoro che include la creazione del corpus, la pre-elaborazione dei dati, l'applicazione di modelli statistico-frequenziali e, infine, l'uso di tecniche di Topic Modelling per identificare e visualizzare i principali temi trattati nel dibattito costituente.

## Fasi del lavoro 
Il progetto è strutturato in tre fasi principali del lavoro:

* Creazione del Corpus:  Il corpus è stato ottenuto tramite web scraping, raccogliendo i discorsi dell'Assemblea Costituente. Una volta raccolto, il corpus è stato normalizzato per garantire che il testo fosse coerente e pronto per l'analisi.

* Analisi Statistico/Frequenziale: L'analisi prevede l'esplorazione del corpus attraverso tecniche statistiche e frequenziali per identificare le parole e i concetti più ricorrenti.

* Topic Modelling : viene utilizzato il topic modelling per estrarre argomenti latenti e capire le principali tematiche trattate nel dibattito.

## Documentazione 
La repository contiene i seguenti documenti e le seguenti cartelle:

*assemblea* : la cartella contiene i file .txt delle relazioni che compongono il corpus. Questo è l'output otenuto tramite web swcraping e normalizzazione del testo. 

*code* : scrpit del progetto

*output* : Gli output sono file risultanti dall'esecuzione dello script. La cartella contiene 3 file HTML, uno per il barplot delle parole più frequenti, uno per l'analisi nell'andamento temporale delle parole significaive TF-IDF, uno per l'infografica del Topic Model. All'interno vi è anche una cartella relativa al modello per il Topic Model, contenente corpus e dizionario.

*doc* : La cratella contiente il report descrittivo del progetto e una relazionbe che riassume e analizza i risulati ottenuti. 

*requirements.txt* : dipendenze del progetto Python.

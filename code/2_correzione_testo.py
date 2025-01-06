import os
import re
import time

start_time = time.time()

def correggi_apostrofi(text):
    """Correggi la codifica testuale in base alle regole specificate."""
    # gestione del caso speciale "po'"
    text = re.sub(r"\bpo'", "po'", text)

    # trasformazione dell'apostrofo in accento se preceduto da vocale
    text = re.sub(r"([aeiou])'", r"\1̀", text)  # sostituzione dell'apostrofo con accento sulla vocale

    # mantenere l'apostrofo, ma rimuovi il carattere dopo l'apostrofo se è preceduto da consonante
    text = re.sub(r"([bcdfghlmnpqrstvwxyz])'.", r"\1'", text)

    return text

def process_file(file_path):
    """Processa il file specificato: rimuove le prime 7 righe, converte il testo in minuscolo e corregge la codifica testuale."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # rimozione dei metadati
    lines = lines[7:]

    # cncatenazione dele righe (readlines) in una singola stringa
    content = ''.join(lines)

    content = content.lower()

    content = correggi_apostrofi(content)

    # sovrascrivere il file con il contenuto modificato
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(directory_path):
    """Processa tutti i file .txt nella directory specificata."""
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  
            file_path = os.path.join(directory_path, filename)
            process_file(file_path)
            print(f"File processato: {filename}")


directory_path = "assemblea"
process_directory(directory_path)

end_time = time.time()
execution_time = end_time - start_time
print(f'Tempo totale di esecuzione: {execution_time:.2f} secondi')

# Tempo totale di esecuzione: 1.91 secondi

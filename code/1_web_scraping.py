import requests
from bs4 import BeautifulSoup
import os
import time
import string

# necessario scomporre il link
# perchè i link ai doc e alla pagina successiva hanno necessità di essere riuniti con base_url per essere input delle funzioni
base_url = 'https://bdp.camera.it'
list_url = f'{base_url}/init/cost/lista'
output_dir = 'assemblea'  

os.makedirs(output_dir)

def get_document_links(page_url):
    """Estrarre i link dei documenti dalla pagina web"""
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # trovare tutti i link dei documenti
    links = soup.find_all('a', href=True)
    document_links = [link['href'] for link in links if link['href'].startswith('/init/cost/scheda/')]
    
    return document_links, soup

def extract_content(url, retries=3):
    """Estrarre i contenuti dal link"""
    for _ in range(retries):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text_elements = soup.find_all('td', class_='w2p_fw')
            return [element.get_text(strip=True) for element in text_elements]

def get_next_page(soup):
    """Trova il link alla pagina successiva"""
    next_page_link = soup.find('a', string=' pagina successiva')
    # non find_all perchè il link alla pagina successiva è uno per pagina
    # si ricerca l'elemento <a> con uno specifico contenuto di testo
    # di cui si estrae l'attributo href che corrisponde al link
    if next_page_link:
        return next_page_link['href']
    return None


start_time = time.time()

all_document_links = []
current_page_url = list_url
found_target_document = False # serve per uscire dal ciclo
#l'opertaore booleao diventa vero quando trova l'ultimo documento di interesse

# iterare su tutte le pagine per estrarre i link dei documenti
while current_page_url and not found_target_document:
    document_links, soup = get_document_links(current_page_url)
    all_document_links.extend(document_links)
    # extend e non append perchèo ogni elemento viene inserito singolarmente
    # append avrebbe inserito la lista come elemento singolo
    
    # trovare il link alla pagina successiva
    next_page_relative = get_next_page(soup)
    current_page_url = f'{base_url}{next_page_relative}' if next_page_relative else None

# iterare sui link dei documenti ed estrarre i contenuti
for link in all_document_links:
    document_url = f'{base_url}{link}'
    content = extract_content(document_url)
    
    # sapendo che ID = prima riga, data = la terza riga e il relatore = settima riga
    document_id = content[0] 
    data_seduta = content[2] 
    relatore = content[6] 
    
    # rimuovere i caratteri problematici per i nomi dei file
    document_id = "".join(c for c in document_id if c.isalnum() or c in (' ', '-')).replace(' ', '_')
    data_seduta = "".join(c for c in data_seduta[0:8] if c.isalnum() or c in (' ', '-')).replace(' ', '_')
    relatore = "".join(c for c in relatore if c.isalnum() or c in (' ', '-'))
    for i, c in enumerate(relatore):
        if c in string.punctuation:
            relatore = relatore[:i]  # prendere tutto fino al primo carattere di punteggiatura
        break
    relatore = relatore.replace(' ', '-')
    
    file_name = os.path.join(output_dir, f'{document_id}_{data_seduta}_{relatore}.txt')
    
 
    with open(file_name, 'w', encoding='utf-8') as file:
        for text in content:
            file.write(text + '\n')
    
    # controllare se l'ID inizia con '4736' e interrompe il ciclo dopo aver salvato il documento
    if document_id.startswith('4736'):
        found_target_document = True
        break  


end_time = time.time()
execution_time = end_time - start_time
print(f'Tempo totale di esecuzione: {execution_time:.2f} secondi')

print(f'Documenti salvati nella directory: {output_dir}')

# Tempo totale di esecuzione: 1676.38 secondi = 27.9 minuti

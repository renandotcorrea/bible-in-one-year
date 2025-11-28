import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import json

bible_books = {
    "gn": "Gênesis",
    "ex": "Êxodo",
    "lv": "Levítico",
    "nm": "Números",
    "dt": "Deuteronômio",
    "js": "Josué",
    "jz": "Juízes",
    "rt": "Rute",
    "1sm": "1 Samuel",
    "2sm": "2 Samuel",
    "1rs": "1 Reis",
    "2rs": "2 Reis",
    "1cr": "1 Crônicas",
    "2cr": "2 Crônicas",
    "ed": "Esdras",
    "ne": "Neemias",
    "et": "Ester",
    "job": "Jó",
    "sl": "Salmos",
    "pv": "Provérbios",
    "ec": "Eclesiastes",
    "ct": "Cantares",
    "is": "Isaías",
    "jr": "Jeremias",
    "lm": "Lamentações",
    "ez": "Ezequiel",
    "dn": "Daniel",
    "os": "Oséias",
    "jl": "Joel",
    "am": "Amós",
    "ob": "Obadias",
    "jn": "Jonas",
    "mq": "Miquéias",
    "na": "Naum",
    "hc": "Habacuque",
    "sf": "Sofonias",
    "ag": "Ageu",
    "zc": "Zacarías",
    "ml": "Malaquias",
    "mt": "Mateus",
    "mc": "Marcos",
    "lc": "Lucas",
    "jo": "João",
    "at": "Atos",
    "rm": "Romanos",
    "1co": "1 Coríntios",
    "2co": "2 Coríntios",
    "gl": "Gálatas",
    "ef": "Efésios",
    "fp": "Filipenses",
    "cl": "Colossenses",
    "1ts": "1 Tessalonicenses",
    "2ts": "2 Tessalonicenses",
    "1tm": "1 Timóteo",
    "2tm": "2 Timóteo",
    "tt": "Tito",
    "fm": "Filemom",
    "hb": "Hebreus",
    "tg": "Tiago",
    "1pe": "1 Pedro",
    "2pe": "2 Pedro",
    "1jo": "1 João",
    "2jo": "2 João",
    "3jo": "3 João",
    "jd": "Judas",
    "ap": "Apocalipse"
}

ep_books = {
    '1': 'O Grande Conflito',
    '2': 'Patriarcas e Profetas',
    '3': 'Profetas e Reis',
    '4': 'O Desejado de Todas as Nações',
    '5': 'Atos dos Apóstolos',
    '33': 'Parábolas de Jesus',
}


def get_today_bible_reading_url():
    base_bible_url = "https://pesquisa.biblia.com.br/pt-BR/NVI/"

    page = requests.get(base_bible_url)

    soup = BeautifulSoup(page.text, "html.parser")

    scripts = soup.find_all("script")[1].text

    parts = scripts.split('$("#leitura").click(function() {')
    location_line = parts[1].split(");", 1)
    url = location_line[0].split(", ", 1)[1].strip()[1:-1]
    return url

def get_profecy_cap(bible_link):
    caps = {}
    bible_profecy_map_json = open("bible_profecy_map.json")
    bible_profecy_map = json.load(bible_profecy_map_json)
    link_parts = bible_link.split('/')
    bible_caps = link_parts[len(link_parts) - 1].split('-')
    print(bible_caps)
    for seq in range(int(bible_caps[0]), int(bible_caps[len(bible_caps)-1]) + 1):
        infos = bible_profecy_map[bible_books[link_parts[len(link_parts) - 2]]][f'{seq}']
        for inf in infos:
            book_id = get_book_id(inf["book"])
            if book_id in caps:
                if int(inf['cap']) not in caps[book_id]:
                  caps[book_id].append(int(inf['cap']))
            else:
                caps[book_id] = [int(inf['cap'])]

    print(caps)
    return caps

def get_book_id(book):
    for k, v in ep_books.items():
        if v == book:
            return k

def resume_message(bible_link, book_info):
    link_parts = bible_link.split('/')
    text_book_caps = ''
    for k,v in book_info.items():
        book_id = k
        book_caps = v
        break
    for cap in book_caps:
        if len(text_book_caps) > 0:
            text_book_caps += ' e'
        text_book_caps += f' {cap}'
    text = f'*Ano Bíblico:*\n\nLeitura de hoje:\n - {bible_books[link_parts[len(link_parts) - 2]]} {link_parts[len(link_parts) - 1]}\n - {ep_books[book_id]} cap.{text_book_caps}'
    return text

def get_profecy(book_info):
    base_url = 'https://ellenwhite.cpb.com.br'
    book_path = 'livro/index'
    links = {}

    for k,v in book_info.items():
        book_id = k
        captule = v
        break

    page  = requests.get(f'{base_url}/{book_path}/{book_id}')
    soup = BeautifulSoup(page.text, "html.parser")
    uls = soup.find_all("ul", {"class": "sumario"})

    for litag in uls[0].find_all('li'):
        for cap in captule:
            if f'Capítulo {cap} ' in litag.text:
                links[cap] = f'{base_url}{litag.find_all("a", href=True)[0]["href"]}'

    return links

def profecy_message(book_captules):
    for k,v in book_captules.items():
        book_id = k
        break
    profecy_links = get_profecy(book_captules)
    cap_text = ''
    for k,v in profecy_links.items():
        cap_text += f' - {ep_books[book_id]} cap. {k}: {v}\n'

    return f'*Espírito de Profecia:*\n\n{cap_text}'


if __name__ == '__main__':
    bible_link = get_today_bible_reading_url()
    print("Today's Bible Reading Link:", bible_link)
    profecy_caps = get_profecy_cap(bible_link)
    print("Prophecy Chapters:", profecy_caps)
    message = resume_message(bible_link, profecy_caps)
    print(message)
    profecy_links_message = profecy_message(profecy_caps)
    print(profecy_links_message)

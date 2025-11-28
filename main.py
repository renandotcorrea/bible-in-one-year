import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

def get_today_bible_reading_url():
    base_bible_url = "https://pesquisa.biblia.com.br/pt-BR/NVI/"

    page = requests.get(base_bible_url)

    soup = BeautifulSoup(page.text, "html.parser")

    scripts = soup.find_all("script")[1].text

    parts = scripts.split('$("#leitura").click(function() {')
    location_line = parts[1].split(");", 1)
    url = location_line[0].split(", ", 1)[1].strip()[1:-1]
    return url

if __name__ == '__main__':
    print ("Bible URL:", get_today_bible_reading_url())

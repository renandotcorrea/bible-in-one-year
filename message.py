from scrapper import bible_books, ep_books, get_profecy_links

def resume_message(bible_link, book_info):
    link_parts = bible_link.split('/')
    text_book_caps = ''
    for k, v in book_info.items():
        book_id = k
        book_caps = v
        break

    for cap in book_caps:
        if len(text_book_caps) > 0:
            text_book_caps += ' e'
        text_book_caps += f' {cap}'
    text = f'*Ano Bíblico:*\n\nLeitura de hoje:\n - {bible_books[link_parts[len(link_parts) - 2]]} {link_parts[len(link_parts) - 1]}\n - {ep_books[book_id]} cap.{text_book_caps}'
    return text


def profecy_message(book_captules):
    for k, v in book_captules.items():
        book_id = k
        break
    profecy_links = get_profecy_links(book_captules)
    cap_text = ''
    for k, v in profecy_links.items():
        cap_text += f' - {ep_books[book_id]} cap. {k}: {v}\n'

    return f'*Espírito de Profecia:*\n\n{cap_text}'


def bible_message(bible_link):
    link_parts = bible_link.split('/')
    text = f'*Bíblia:*\n\n - {bible_books[link_parts[len(link_parts) - 2]]} {link_parts[len(link_parts) - 1]}: {bible_link}'
    return text

import requests
from bs4 import BeautifulSoup



def get_html(link):
    response = requests.get(link).text
    return response

def get_field(soup, find_tag, param_dict=None):
    try:
        field = soup.find(find_tag, param_dict).text
    except AttributeError:
        field = '...'
    return field


def get_info(parse_text):
    soup = BeautifulSoup(parse_text, 'html.parser')

    title = get_field(soup, 'title')
    bath = get_field(soup, 'li', {'class': 'parnv'})
    seats = get_field(soup, 'li', {'class': 'mes'})
    bas = get_field(soup, 'li', {'class': 'bas'})
    price = get_field(soup, 'span', {'class': 'kr'})
    adress = get_field(soup, 'li', {'class': 'adr'})
    phone = get_field(soup, 'p', {'class': 'telvn'})


    info = {'title': title,
                'fields': {
                    'bath': bath,
                    'bas': bas,
                    'seats': seats,
                    'price': price,
                    'adress': adress,
                    'phone': phone,
                }
    }
    return info


def get_all_pages_links(link, parse_text):
    link_list = [link]
    soup = BeautifulSoup(parse_text, 'html.parser')
    dirty_obj = soup.find('div', {'class': 'nm'}).find_all('a', href=True)
    slugs_list = [href['href'] for href in dirty_obj]
    for slug in slugs_list[:-1]:
        link_list.append(link + slug)
    return link_list


def get_single_page_links(link, links_list):
    full_list = []
    for l in links_list:
        html = get_html(l)
        soup = BeautifulSoup(html, 'html.parser')
        dirty_links_obj = soup.find('div', {'class': 'spis'}).find_all('a', {'class': 'nazvan'})
        slugs_list = [link + slug.get('href') for slug in dirty_links_obj]
        full_list.extend(slugs_list)
    return full_list


def write_file(text):
    with open('file_dirty_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    link1 = 'http://www.saunaminska.info/druzhnaja.htm'
    link2 = 'http://www.saunaminska.info/'
    html = get_html(link2)
    all_pages = get_all_pages_links(link2, html)
    links_from_single_page = get_single_page_links(link2, all_pages)
    for idx, link in enumerate(links_from_single_page):
        print(f'{idx}. {link}')


    #
    # print(all_pages)
    # write_file(all_pages)
    # proc = get_info(html)
    #
    # print(proc['title'], end='\n\n')
    # for k, v in proc['fields'].items():
    #     print(f'{k} - {v}')

if __name__ == '__main__':
    main()
